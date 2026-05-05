from . import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime
from datetime import datetime

from pwdlib import PasswordHash
#pwdlib
# $pip install ""pwdlib[argon2]

password_hash = PasswordHash.recommended()

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    username: Mapped[str] = mapped_column(String(100))
    _password: Mapped[str] = mapped_column(String(200))

    def __init__(self, *args, **kwargs):
        password =kwargs.pop('password')
        super().__init__(**kwargs)
        if password:
            self.password = password         #raw_password的值其实是传进来passworf


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = password_hash.hash(raw_password)

    def check_password(self, raw_password):
        return password_hash.verify(raw_password, self.password)


class EmailCode(Base):
    __tablename__ = 'email_code'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100))
    code: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)