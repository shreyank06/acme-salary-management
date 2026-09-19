import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, sessionmaker

from app.api import employees, insights
from app.config import settings
from app.database import init_db, make_engine, make_session_factory
from app.errors import ConflictError, NotFoundError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


def create_app(session_factory: sessionmaker[Session] | None = None) -> FastAPI:
    app = FastAPI(title="ACME Salary Management", version="1.0.0")

    if session_factory is None:
        engine = make_engine(settings.database_url)
        init_db(engine)
        session_factory = make_session_factory(engine)
    app.state.session_factory = session_factory

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(NotFoundError)
    async def _not_found(_: Request, exc: NotFoundError):
        return JSONResponse({"detail": str(exc)}, status_code=404)

    @app.exception_handler(ConflictError)
    async def _conflict(_: Request, exc: ConflictError):
        return JSONResponse({"detail": str(exc)}, status_code=409)

    @app.get("/health", tags=["ops"])
    def health():
        return {"status": "ok"}

    app.include_router(employees.router)
    app.include_router(insights.router)
    return app

