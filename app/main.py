from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from models import ImportsRequest

app = FastAPI()


@app.exception_handler(RequestValidationError)
def handle_validation_error(request, exc) -> JSONResponse:
    return JSONResponse(status_code=400, content={"code": 400, "message": "Validation Failed"})


@app.post("/imports")
async def imports(request: ImportsRequest = Body(...)):
    print(request.json())
    return 200


@app.get("/sales")
async def sales(date: str):
    print(date)
    return 200

