from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from settings import Settings

async_engine = create_async_engine(url=Settings.POSTGRES_URL_ASYNC, echo=Settings.POSTGRES_ECHO)
engine = create_engine(url=Settings.POSTGRES_URL, echo=Settings.POSTGRES_ECHO)
async_session_factory = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False, future=True)
session_factory = sessionmaker(bind=engine, class_=Session, expire_on_commit=False, future=True)

AsyncSessionFactory = scoped_session(session_factory=async_session_factory)
SessionFactory = scoped_session(session_factory=session_factory)
