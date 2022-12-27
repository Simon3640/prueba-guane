from fastapi import APIRouter

from app.models import User

router = APIRouter()

@router.post('/')
def hello_world():
    return {'msg': 'Hello world'}


@router.get('/')
async def get_users():
    return await User.all()