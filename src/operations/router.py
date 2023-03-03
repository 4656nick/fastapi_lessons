from datetime import datetime
from sys import prefix
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import operation

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


class operation_model(BaseModel):
    id: int
    quantity: int
    figi: str
    instrument_type: str
    date: datetime
    type: str

    class Config:
        orm_mode = True


@router.get("/")
async def get_specific_operations(
        operation_type: str,
        session: AsyncSession = Depends(get_async_session))\
        -> List[operation_model]:
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    return result.all()
