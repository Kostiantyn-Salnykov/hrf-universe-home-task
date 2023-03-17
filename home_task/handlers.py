from fastapi import Request, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError, NoResultFound

from home_task.enums import JSENDStatus
from home_task.exceptions import BackendException
from settings import Settings


def backend_exception_handler(request: Request, exc: BackendException) -> ORJSONResponse:
    """
    Handler for BackendException.

    Args:
        request (Request): FastAPI Request instance.
        exc (BackendException): Error that Back-end raises.

    Returns:
        result (ORJSONResponse): Transformed JSON response from Back-end exception.
    """
    return ORJSONResponse(content=exc.dict(), status_code=exc.code)


def integrity_error_handler(error: IntegrityError) -> None:
    """
    Handler for IntegrityError (SQLAlchemy error).

    Args:
        error (IntegrityError): Error that SQLAlchemy raises (in case of SQL query error).

    Raises:
        BackendException: Actually proxies these errors to `backend_exception_handler`.
    """
    if "duplicate" in error.args[0]:
        # Parse duplication error and show it in debug mode, otherwise "update error".
        raise BackendException(message=str(error.orig.args[0].split("\n")[-1]) if Settings.DEBUG else "Update error.")
    else:
        raise BackendException(
            message=str(error) if Settings.DEBUG else "Internal server error.",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=JSENDStatus.ERROR,
        )


def no_result_found_error_handler(error: NoResultFound) -> None:
    """
    Handler for NoResultFound (SQLAlchemy error).

    Args:
        error (NoResultFound): Error that SQLAlchemy raises (in case of scalar_one() error).

    Raises:
        BackendException: Actually proxies these errors to `backend_exception_handler`.
    """
    raise BackendException(
        message="Not found.",
        code=status.HTTP_404_NOT_FOUND,
        status=JSENDStatus.FAIL,
    )
