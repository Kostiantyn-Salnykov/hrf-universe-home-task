from typing import Optional

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy import text
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession

from home_task.deps import get_async_session
from home_task.schemas import DaysToHireStatisticsOutSchema
from home_task.types import StrUUID

home_task_router = APIRouter(prefix="/home_task")


@home_task_router.get(
    path="/{standardJobID}/",
    name="get_days_to_hire_statistics",
    summary="Get statistics by days to hire.",
    response_model=DaysToHireStatisticsOutSchema,
)
async def get_days_to_hire_statistics(
    db_session: AsyncSession = Depends(get_async_session),
    standard_job_id: StrUUID = Path(alias="standardJobID"),
    country_code: Optional[str] = Query(default=None, max_length=2, alias="countryCode"),
):
    statement = text(
        """
        SELECT * FROM public.days_to_hire_statistics
        WHERE standard_job_id = :standard_job_id AND country_code = :country_code;
        """
    )
    result: ChunkedIteratorResult = await db_session.execute(
        statement=statement, params={"standard_job_id": standard_job_id, "country_code": country_code}
    )
    obj = result.one()
    return DaysToHireStatisticsOutSchema.from_orm(obj=obj)
