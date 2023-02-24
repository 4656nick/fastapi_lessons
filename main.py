from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, status, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, ValidationError
from starlette.responses import JSONResponse

app = FastAPI(
    title="Trading app",
    description="This is a simple trading app",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
)


@app.exception_handler(ValidationError)
def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()})
    )


users = [
    {"id": 1, "role": "admin", "name": ["Bob"]},
    {"id": 2, "role": "investor", "name": "Jane"},
    {"id": 3, "role": "trader", "name": "Martin"},
    {"id": 4, "role": "investor", "name": "Carlos", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"},
    ]},
]

fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12}
]


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in users if user.get("id") == user_id]


@app.get("/trades")
def get_trades(offset: int = 1, limit: int = 1):
    return fake_trades[offset:][:limit]


# fake_users = [
#     {"id": 1, "role": "admin", "name": "Bob"},
#     {"id": 2, "role": "investor", "name": "Jane"},
#     {"id": 3, "role": "trader", "name": "Martin"},
# ]
#
# @app.post("/users/{user_id}")
# def change_user_name(user_id: int, new_name: str):
#     current_user = list(filter(lambda user: user.get("id") == user_id, fake_users))[0]
#     current_user["name"] = new_name
#     return {
#         "status": 200, "data": current_user
#     }

class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post("/trades/")
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {
        "status": 200, "data": fake_trades
    }
