from fastapi import APIRouter, Query, Depends, HTTPException
from pydantic import EmailStr, NameEmail
from typing import Annotated
from dependencies import get_mail, get_session
from fastapi_mail import FastMail, MessageSchema, MessageType
from models import AsyncSession
import string
import random
from aiosmtplib import SMTPResponseException
from repository.user_repo import EmailCodeRepository, UserRepository

from schemas import ResponseOut
from schemas.user_schemas import RegisterIn, UserCreateSchema, LoginIn, LoginOut
from models.user import User

from core.auth import AuthHandler

router = APIRouter(prefix="/auth", tags=["user"])

auth_handler = AuthHandler()

@router.get("/code", response_model=ResponseOut)
async def get_email_code(
    email: Annotated[EmailStr, Query(...)],
    mail: FastMail = Depends(get_mail),
    session: AsyncSession = Depends(get_session),
):
    #1.生成四位数字验证码
    source = string.digits *4
    code = ''.join(random.sample(source, 4))
    #2.创建消息对象
    message = MessageSchema(
        subject="注册验证码",
        recipients=[email],
        body=f"您的验证码为：{code},5分钟内有效",
        subtype=MessageType.plain
    )

    #try,如果捕获了异常才进行if判断！
    try:
        await mail.send_message(message)
    except SMTPResponseException as e:
        if e.code == -1 and b"\\x00\\x00\\x00" in str(e).encode():
            print("有问题")
            #将邮箱和验证码存储到数据库中
        else:
            raise HTTPException(status_code=500, detail="发送失败")

    email_code_repo = EmailCodeRepository(session=session)
    # 所以EmailCodeRepository只是一个普通的类吗？
    await email_code_repo.create(str(email), code)
    #这里是不是先返回return的内容，然后再通过response_model过滤呢？
    return ResponseOut()

@router.post("/register", response_model=ResponseOut)
async def register(
    #为什么默认数据来源body？Annotated[RegisterIn, Body],
    data: RegisterIn,
    session: AsyncSession = Depends(get_session),
):
    user_repo = UserRepository(session=session)
    #1.判断邮箱是否存在
    email_exist = await user_repo.email_is_exist(email=str(data.email))
    if email_exist:
        raise HTTPException(400, detail="该邮箱已经存在")
    #2.校验验证码是否正确
    email_code_repo = EmailCodeRepository(session=session)
    email_code_match =  email_code_repo.check_email_code(email=str(data.email), code=str(data.code))
    if not email_code_match:
        raise HTTPException(400, detail="验证码错误")
    try:
        await user_repo.create(UserCreateSchema(email=str(data.email), password=data.password, username=data.username))
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    return ResponseOut()

@router.post("/login", response_model=LoginOut)
async def login(
    data: LoginIn,
    session: AsyncSession = Depends(get_session),
):
    #1.创建user_repo对象
    user_repo = UserRepository(session=session)
    #2.根据邮箱查找用户
    user: User|None = await user_repo.get_by_email(email=str(data.email))
    if not user:
        raise HTTPException(400, detail="该用户不存在")
    if not user.check_password(data.password):
        raise HTTPException(400, detail="密码错误")
    #3.生成JWT
    tokens = auth_handler.encode_login_token(user.id)
    return {
        #下面的user是一个orm模型，必须通过response_model解析成字典才能传给前端
        "user":user,
        "token":tokens['access_token'],
    }
