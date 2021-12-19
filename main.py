from aiohttp import ClientSession
from Python_ARQ import ARQ
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from uvicorn import run
app = FastAPI()
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"ok":False, "detail": exc.errors()}),
    )




async def main(text: str, lang: str):
    session = ClientSession()
    arq = ARQ("https://thearq.tech", "JCOBCX-IEYTGE-AZFIEP-AYLDTF-ARQ", session)
    results = await arq.translate(text, lang)
    await session.close()
    return results
@app.get("/translate/")
async def root(text: str, lang: str):
    myres = await main(text, lang)
    return {"ok":True, "data" : myres}
