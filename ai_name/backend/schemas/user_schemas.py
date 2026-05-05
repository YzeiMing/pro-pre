from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Annotated, List

UsernameStr = Annotated[str, Field(..., min_length=4, max_length=32, description="用户名")]
RawPasswordStr = Annotated[str, Field(min_length=6, max_length=20, description="密码")]

#用来约束和校验前端上传的数据
class RegisterIn(BaseModel):
    email: EmailStr
    username: UsernameStr
    password: RawPasswordStr
    confirm_password: RawPasswordStr
    code: Annotated[str, Field(..., min_length=4, max_length=4)]

    #校验完数据本身，再去校验其他数据逻辑
    @model_validator(mode="after")
    def password_is_match(self) -> "RegisterIn":
        password = self.password
        confirm_password = self.confirm_password
        if password != confirm_password:
            raise ValueError("密码不一致")
        return self

class UserCreateSchema(BaseModel):
    email: str
    password: RawPasswordStr
    username: UsernameStr

class LoginIn(BaseModel):
    email: EmailStr
    password: RawPasswordStr


class UserSchema(BaseModel):
    id: Annotated[int, Field(...)]
    email: EmailStr
    username: UsernameStr

#就是说schema/basemodel模型的字段类型不可以是base模型类型？
class LoginOut(BaseModel):
    user: UserSchema
    token: str

