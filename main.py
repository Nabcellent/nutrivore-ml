from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import api


def init_server():
    app = FastAPI(title='Nutrivore', description='Nutrivore API', version='1.0.0')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://localhost:3000",
            "https://nutrivore-web-dkuvi4xfka-uc.a.run.app",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api.router, prefix='/api', tags=['API'])

    return app


server = init_server()


@server.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc):
    errors = []
    for error in exc.errors():
        detail = {
            "loc": list(error["loc"]),
            "msg": error["msg"],
        }
        errors.append(detail)

    return JSONResponse(
        status_code=422,
        content={"message": f'{errors[0]["loc"][1]}: {errors[0]["msg"]}', "errors": errors},
    )


@server.get("/")
def home():
    return {"health_check": "OK"}
