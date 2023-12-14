from datetime import datetime, timedelta
from typing import Annotated

import constants
import jwt
import services
import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from models.models import AuthUser, Feedback, Product, User

my_app = FastAPI()
security = HTTPBasic()
SECRET_KEY = "secure_stored_secret_key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_jwt")

# imitations of Data Base
auth_user_db = [AuthUser(username=user["name"], password=user["password"]) for user in constants.user_db]


def get_user_from_auth_user_db(username: str):
    for user in auth_user_db:
        if user.username == username:
            return user
    return None


# end of imitation


@my_app.get("/")
async def root():
    return FileResponse("HighProgrammingSchool/lessons/fastAPI/templates/index.html")


@my_app.post("/user")
async def post_user(user: User) -> User:
    user_json = user.model_dump()
    user_json.update(
        {
            "is_adult": services.is_adult(user.age),
        }
    )
    return user_json


@my_app.get("/users")
async def get_users() -> User:
    test_user = User(
        name="John Doe",
        id=1,
    )
    return test_user


@my_app.post("/feedback")
async def create_feedback(feedback: Feedback) -> Feedback:
    ind = max(constants.feedback_db.keys()) if constants.feedback_db.keys() else 0
    ind += 1
    constants.feedback_db.update({ind: feedback})
    return feedback


@my_app.get("/product/{product_id}")
async def get_product(product_id: int) -> Product | dict:
    product_models_list = []
    for attributes in constants.sample_products:
        product_models_list.append(Product(**attributes))
    product_filtered = list(filter(lambda product: product.product_id == product_id, product_models_list))
    if not product_filtered:
        return {"error": "Not found"}
    return product_filtered[0]


@my_app.get("/products/search")
async def search_product(keyword: str, category: str = None, limit: int = 10) -> list[Product]:
    product_models_list = []
    for attributes in constants.sample_products:
        product_models_list.append(Product(**attributes))
    product_filtered = list(filter(lambda product: keyword in product.name, product_models_list))
    if category:
        product_filtered = list(filter(lambda product: product.category == category, product_filtered))
    return product_filtered[:limit]


async def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_auth_user_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


@my_app.post("/login_base")
async def login_base(auth_user: AuthUser = Depends(authenticate_user)) -> Response:
    return Response("You got my secret, welcome")


@my_app.post("/login_cookie")
async def login_cookie(auth_user: AuthUser, response: JSONResponse) -> Response:
    found_user_filtered = list(filter(lambda user: user["name"] == auth_user.username, constants.user_db))
    if not found_user_filtered:
        return Response("User not found", 404)
    user = found_user_filtered[0]
    if user["password"] != auth_user.password:
        return Response("Password invalid", 401)
    user["token"] = f"asd123qwe432{user['id']}"
    response.set_cookie(
        key="session_token", value=f"asd123qwe432{user['id']}", max_age=60 * 10, httponly=True  # secure=True,
    )
    response.body = jsonable_encoder({"message": "куки установлены"})
    response.status_code = 200
    return response.body


@my_app.get("/current_user")
async def get_current_user(request: Request) -> User:
    session_token = request.cookies.get("session_token")
    if session_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_filtered = list(filter(lambda user: user.get("token", False) == session_token, constants.user_db))
    if user_filtered:
        return User(**user_filtered[0])
    return Response("Nop")


@my_app.get("/headers")
async def get_headers(
    request: Request,
    user_agent: Annotated[str | None, Header()] = None,
    accept_language: Annotated[str | None, Header()] = None,
) -> JSONResponse:
    if user_agent is None or accept_language is None:
        missed_headers = []
        if user_agent is None:
            missed_headers.append("User-Agent")
        if accept_language is None:
            missed_headers.append("Accept-Language")
        raise HTTPException(status_code=404, detail=f"Header(s) {', '.join(missed_headers)} not found")
    return JSONResponse(content={"User-Agent": user_agent, "Accept-Language": accept_language})


def create_jwt_token(data: dict) -> str:
    data.update({"exp": datetime.utcnow() + timedelta(minutes=1)})

    # кодируем токен, передавая в него наш словарь с тем, что мы хотим там разместить
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


@my_app.post("/login_jwt")
async def login_jwt(user_auth: AuthUser) -> JSONResponse:
    user = get_user_from_auth_user_db(user_auth.username)
    if user and user.password == user_auth.password:
        return JSONResponse(
            content={"access_token": create_jwt_token({"sub": user_auth.username}), "token_type": "bearer"}
        )
    raise HTTPException(detail="Invalid credentials", status_code=401)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # декодируем токен
        # тут мы идем в полезную нагрузку JWT-токена и возвращаем утверждение о юзере (subject);
        # обычно там еще можно взять "iss" - issuer/эмитент, или "exp" - expiration time - время 'сгорания' и другое,
        # что мы сами туда кладем
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        # тут какая-то логика ошибки истечения срока действия токена
        raise HTTPException(detail="Token expired", status_code=400)
    except jwt.InvalidTokenError:
        pass  # тут какая-то логика обработки ошибки декодирования токена


@my_app.get("/jwt_protected_resource")
async def get_jwt_protected(current_user: str = Depends(get_user_from_token)):
    user = get_user_from_auth_user_db(current_user)
    if user:
        return Response("Access granted")
    raise HTTPException(detail="Access denied", status_code=401)


if __name__ == "__main__":
    # console command: uvicorn main:my_app --reload --port 8001
    uvicorn.run(
        "main:my_app",
        host="127.0.0.1",
        port=8001,
        reload=True,
    )
