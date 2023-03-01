from fastapi import FastAPI, status, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_users import FastAPIUsers
from pydantic import ValidationError
from starlette.responses import JSONResponse

from src.database import User
from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

app = FastAPI(
    title="Trading app",
    description="This is a simple trading app",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.exception_handler(ValidationError)
def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()})
    )


# class DegreeType(Enum):
#     newbie = "newbie"
#     expert = "expert"


# class Degree(BaseModel):
#     id: int
#     created_at: datetime
#     type_degree: DegreeType


# @app.get("/users/{user_id}", response_model=List[User])
# def get_user(user_id: int):
#     return [user for user in users if user.get("id") == user_id]


# @app.get("/trades")
# def get_trades(offset: int = 1, limit: int = 1):
#     return fake_trades[offset:][:limit]


# class Trade(BaseModel):
#     id: int
#     user_id: int
#     currency: str = Field(max_length=5)
#     side: str
#     price: float = Field(ge=0)
#     amount: float


# @app.post("/trades/")
# def add_trades(trades: List[Trade]):
#     fake_trades.extend(trades)
#     return {
#         "status": 200, "data": fake_trades
#     }

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

@app.get("/unprotected-route")
def protected_route():
    return f"Hello, anonymous"
