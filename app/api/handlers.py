from typing import Union
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import *
from ..db.dals import UserDAL
from ..db.session import get_db

user_router = APIRouter()  # создание router для User




