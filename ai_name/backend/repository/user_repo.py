from models import AsyncSession
from models.user import EmailCode
from sqlalchemy import select, exists

from datetime import datetime, timedelta

from schemas.user_schemas import UserCreateSchema
from models.user import User

class EmailCodeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, email: str, code: str) -> EmailCode:
        async with self.session.begin():
            email_code = EmailCode(email=email, code=code)
            self.session.add(email_code)
            #为什么返回就可以执行commit操作？
            return email_code

    async def check_email_code(self, email: str, code: str) -> EmailCode:
        async with self.session.begin():
            #这是怎么判断的？
            stmt = select(EmailCode).where(EmailCode.email == email, EmailCode.code == code)
            email_code: EmailCode | None = await self.session.scalar(stmt)
            if not email_code:
                return False
            if (datetime.now() - email_code.created_at) < timedelta(minutes=10):
                return False
            return True


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User|None:
        async with self.session.begin():
            return await self.session.scalar(select(User).filter(User.email == email))

    async def email_is_exist(self, email: str) -> bool:
        async with self.session.begin():
            stmt = select(exists().where(User.email == email))
            return await self.session.scalar(stmt)

    async def create(self, user_schema: UserCreateSchema) -> User:
        async with self.session.begin():
            #model_dump转换为字典，**则将字典拆解为关键字参数
            user = User(**user_schema.model_dump())
            #为什么这里不需要await
            self.session.add(user)
            return user
