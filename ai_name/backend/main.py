from fastapi import FastAPI
from fastapi_mail import FastMail, MessageSchema, MessageType, NameEmail
from fastapi import Depends

from dependencies import get_mail
from aiosmtplib import SMTPResponseException

from router.auth_router import router as auth_router
from router.name_router import router as name_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(name_router)



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/mail/test")
async def mail_test(
        email: NameEmail,
        mail: FastMail = Depends(get_mail),
):
    message = MessageSchema(
        subject="hello",
        recipients = [email],
        body=f"hello {email}",
        subtype = MessageType.plain,
    )
    try:
        await mail.send_message(message)
    except SMTPResponseException as e:
        if e.code == -1 and b"\\x00\\x00\\x00" in str(e).encode():
            print("有问题")
    return {"message": "邮件发送成功"}
