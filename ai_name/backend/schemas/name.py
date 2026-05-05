#只是用来给路由函数的数据的输入输出进行数据验证，而agent是针对ai模型工具的数据验证


from pydantic import BaseModel, Field
from typing import Annotated, List, Literal
from .agent import NameSchema

class NameIn(BaseModel):
    surname: Annotated[str, Field(..., description="姓氏")]
    gender: Annotated[Literal["不限", "男", "女"], Field(..., description="性别")]
    length: Annotated[Literal["不限", "单字", "两字"], Field(..., description="字数")]
    other: Annotated[str|None, Field('', description="其他要求")]
    exclude: Annotated[List[str], Field([], description="排除的名字")]

#这里的nameout和nameresultlist的一样？有什么用？
class NameOut(BaseModel):
    name: List[NameSchema]
