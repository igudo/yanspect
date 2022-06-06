from fastapi import FastAPI

app = FastAPI()


@app.post("/test", status_code=200)
async def test():
    return 200
