from fastapi import APIRouter, Depends
from schemas.name import NameIn, NameOut
from core.agent import generate_names

from core.auth import AuthHandler

auth_handler = AuthHandler()

router = APIRouter(prefix="/name", tags=["name"])


@router.post("/", response_model=NameOut)
async def take_names(
    data: NameIn,
    user_id: int=Depends(auth_handler.auth_access_dependency)
):
    name_result = await generate_names(data)
    #这里为什么需要这么麻烦呢？nameout和nameresultschema的nams？
    #{"name": [{"name":"xx", "reference": "xx", moral: "xx"}]}
    return NameOut(name=name_result.name)