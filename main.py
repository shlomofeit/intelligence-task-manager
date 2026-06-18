from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from database.db_connection import DBConnection
from routes.agent_routes import router as agent_router
from routes.mission_routes import router as mission_router
from routes.mission_routes import router as report_router
from logging_base import logger
from contextlib import asynccontextmanager

# print(DBConnection.connect())
# conn = DBConnection.get_connection()
# print(conn)
# # conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = DBConnection.get_connection()
    yield
    conn.close()

app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def request_logger(req: Request, call_next):
    logger.info("%s %s called", req.method, req.url)
    response = await call_next(req)

    return response


app.include_router(agent_router, prefix="/agents", tags=["Agents"])

app.include_router(mission_router, prefix="/missions", tags=["Missions"])

app.include_router(report_router, prefix="/reports", tags=["Reports"])


# if __name__ == '__main__':
#     main()