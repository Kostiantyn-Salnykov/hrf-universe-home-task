from sqlalchemy.exc import IntegrityError, NoResultFound

from home_task.db import async_session_factory
from home_task.handlers import integrity_error_handler, no_result_found_error_handler


async def get_async_session():
    """Creates FastAPI dependency for generation of SQLAlchemy AsyncSession.

    Yields:
        AsyncSession: SQLAlchemy AsyncSession.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except IntegrityError as error:
            await session.rollback()
            integrity_error_handler(error=error)
        except NoResultFound as error:
            await session.rollback()
            no_result_found_error_handler(error=error)
        finally:
            await session.close()
