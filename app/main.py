import fastapi
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from models import ImportsRequest, Error, StatusCode, ResponseContent
from exceptions import NotFoundException
from controllers import ImportsController, DeleteController, NodesController, SalesController
from repositories import DBRepository
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

app = FastAPI()
db = None


@app.on_event("startup")
async def startup():
    """При запуске инициализируем базу данных"""
    global db
    import os
    db_host = os.environ.get("DATABASE_HOST")
    db_port = os.environ.get("DATABASE_PORT")
    db_name = os.environ.get("DATABASE_NAME")
    db_user = os.environ.get("DATABASE_USER")
    db_password = os.environ.get("DATABASE_PASSWORD")
    db_offers_table_name = os.environ.get("DB_OFFERS_TABLE_NAME")
    db_categories_table_name = os.environ.get("DB_CATEGORIES_TABLE_NAME")
    db_history_table_name = os.environ.get("DB_HISTORY_TABLE_NAME")
    db = DBRepository(db_host, db_name, db_user, db_password, db_port)
    db.history_table_name = db_history_table_name
    db.categories_table_name = db_categories_table_name
    db.offers_table_name = db_offers_table_name
    db.create_tables()

    # DEBUG!!!!!!
    db._execute("DELETE FROM "+db.offers_table_name)
    db._execute("DELETE FROM "+db.categories_table_name)
    db._execute("DELETE FROM "+db.history_table_name)

@app.get("/test1")
def test1():
    print(db.select(db.offers_table_name))
    print(db.select(db.categories_table_name))
    print(db.select(db.history_table_name))


@app.on_event("shutdown")
def shutdown_event():
    db.close()


@app.exception_handler(RequestValidationError)
async def handle_validation_error(request: fastapi.Request, exc: RequestValidationError) -> JSONResponse:
    """Переопределяет Validation Error в соответсвии с openapi.yaml;
    код по умолчанию 422 в fastapi"""
    logger.error(f"RequestValidationError {request.url}: {exc.raw_errors}")
    return JSONResponse(
        status_code=StatusCode.BAD_REQUEST_400,
        content=Error(code=StatusCode.BAD_REQUEST_400, message="Validation Failed").dict()
    )


@app.exception_handler(NotFoundException)
async def handle_validation_error(request: fastapi.Request, exc: NotFoundException) -> JSONResponse:
    """Переопределяет Validation Error в соответсвии с openapi.yaml;
    код по умолчанию 422 в fastapi"""
    logger.error(f"NotFoundException {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=StatusCode.NOT_FOUND_404,
        content=Error(code=StatusCode.NOT_FOUND_404, message="Item not found").dict()
    )


@app.post("/imports")
async def imports(request: ImportsRequest = Body(...)):
    """Импортирует новые товары и/или категории. Товары/категории импортированные повторно обновляют текущие.
    Изменение типа элемента с товара на категорию или с категории на товар не допускается. Порядок элементов в
    запросе является произвольным. """
    r = ImportsController(db).import_items(request)
    code = StatusCode.OK_200 if type(r) == bool and r else StatusCode.BAD_REQUEST_400
    return JSONResponse(
        status_code=code,
        content=ResponseContent(code=code, message="success" if code==StatusCode.OK_200 else "wrong input").dict()
    )


@app.delete("/delete/{id}")
async def delete(id: str):
    """Удалить элемент по идентификатору. При удалении категории удаляются все дочерние элементы. Доступ к статистике
    (истории обновлений) удаленного элемента невозможен. """
    r = DeleteController(db).delete(id)
    code = StatusCode.OK_200 if type(r) == bool and r else StatusCode.BAD_REQUEST_400
    return JSONResponse(
        status_code=code,
        content=ResponseContent(code=code, message="success" if code==StatusCode.OK_200 else "wrong").dict()
    )


@app.get("/nodes/{id}")
async def nodes(id: str):
    """Удалить элемент по идентификатору. При удалении категории удаляются все дочерние элементы. Доступ к статистике
    (истории обновлений) удаленного элемента невозможен. """
    r = NodesController(db).nodes(id)
    code = StatusCode.OK_200 if type(r) == dict and r else StatusCode.BAD_REQUEST_400
    return JSONResponse(
        status_code=code,
        content=(r if code==StatusCode.OK_200 else ResponseContent(code=code, message="wrong").dict())
    )


@app.get("/node/{id}/statistic")
async def statistic(id: str, dateStart: str, dateEnd: str):
    """Получение списка **товаров**, цена которых была обновлена за последние 24 часа от времени переданном в
    запросе. Обновление цены не означает её изменение. Обновления цен удаленных товаров недоступны. При обновлении
    цены товара, средняя цена категории, которая содержит этот товар, тоже обновляется. """
    r = NodesController(db).statistic(id, dateStart, dateEnd)
    code = StatusCode.OK_200 if type(r) == dict and r else StatusCode.BAD_REQUEST_400
    return JSONResponse(
        status_code=code,
        content=(r if code == StatusCode.OK_200 else ResponseContent(code=code, message="wrong").dict())
    )


@app.get("/sales")
async def sales(date: str):
    """Получение списка **товаров**, цена которых была обновлена за последние 24 часа от времени переданном в
    запросе. Обновление цены не означает её изменение. Обновления цен удаленных товаров недоступны. При обновлении
    цены товара, средняя цена категории, которая содержит этот товар, тоже обновляется. """
    r = SalesController(db).sales(date)
    code = StatusCode.OK_200 if type(r) == dict and r else StatusCode.BAD_REQUEST_400
    return JSONResponse(
        status_code=code,
        content=(r if code == StatusCode.OK_200 else ResponseContent(code=code, message="wrong").dict())
    )

