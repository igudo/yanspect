from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from models import ImportsRequest, Error, StatusCode
from controllers import ImportsController

app = FastAPI()


@app.exception_handler(RequestValidationError)
def handle_validation_error(request, exc) -> JSONResponse:
    """Переопределяет Validation Error в соответсвии с openapi.yaml;
    код по умолчанию 422 в fastapi"""
    return JSONResponse(
        status_code=400,
        content=Error(code=StatusCode.BAD_REQUEST_400, message="Validation Failed").dict()
    )


@app.post("/imports")
async def imports(request: ImportsRequest = Body(...)):
    """Импортирует новые товары и/или категории. Товары/категории импортированные повторно обновляют текущие.
    Изменение типа элемента с товара на категорию или с категории на товар не допускается. Порядок элементов в
    запросе является произвольным. """
    return ImportsController("db", "yanspect", "root", "root").import_items(request)


@app.get("/sales")
async def sales(date: str):
    """Получение списка **товаров**, цена которых была обновлена за последние 24 часа от времени переданном в
    запросе. Обновление цены не означает её изменение. Обновления цен удаленных товаров недоступны. При обновлении
    цены товара, средняя цена категории, которая содержит этот товар, тоже обновляется. """
    print(date)
    return 200

