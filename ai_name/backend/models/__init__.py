from settings import DB_URI

from sqlalchemy.ext.asyncio import create_async_engine

#from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData



engine = create_async_engine(
    DB_URI,
    #将输出所有执行sql的日志
    echo=True,
    #连接池大小
    pool_size=10,
    #允许连接池最大连接数
    max_overflow=20,
    #获得连接超时时间
    pool_timeout=10,
    #连接回收时间
    pool_recycle=3600,
    #连接前是否预检查
    pool_pre_ping=True,
)

AsyncSessionFactory = async_sessionmaker(
    #Engine或者其子类对象
    bind = engine,
    #Session类的替代
    class_=AsyncSession,
    #是否在查找之前执行flush操作
    autoflush = True,
    #是否在执行commit操作后Session就过期
    expire_on_commit=False,
)

#??????????
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
    # ix: index，索引。
    "ix": 'ix_%(column_0_label)s',
    # uq：unique，唯一约束
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    # ck：Check，检查约束
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    # fk：Foreign Key，外键约束
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    # pk：Primary Key，主键约束
    "pk": "pk_%(table_name)s"
    })


#在下面导入需要迁移的models
from . import user