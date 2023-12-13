from typing import Annotated

import constants
import services
import uvicorn
from fastapi import FastAPI, Header, HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse
from models.models import AuthUser, Feedback, Product, User

my_app = FastAPI()


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


@my_app.post("/login")
async def login(auth_user: AuthUser, response: JSONResponse) -> Response:
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


if __name__ == "__main__":
    # console command: uvicorn main:my_app --reload --port 8001
    uvicorn.run(
        "main:my_app",
        host="127.0.0.1",
        port=8001,
        reload=True,
    )
