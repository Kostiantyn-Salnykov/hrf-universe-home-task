import datetime
import uuid
from typing import Optional

import orjson
import pydantic.json
from pydantic import BaseModel, Field

from home_task.helpers import orjson_dumps


class BaseInSchema(BaseModel):
    """Base schema for schemas that will be used in request validations."""

    class Config:
        """Schema configuration."""

        orm_mode = True
        arbitrary_types_allowed = True
        validate_assignment = True
        allow_population_by_field_name = True
        use_enum_values = True


class BaseOutSchema(BaseInSchema):
    """Base schema for schemas that will be used in responses."""

    class Config(BaseInSchema.Config):
        """Schema configuration."""

        json_encoders = {
            # field type: encoder function
            datetime.timedelta: lambda time_delta: pydantic.json.timedelta_isoformat(time_delta),
            uuid.UUID: str,
        }
        json_dumps = orjson_dumps
        json_loads = orjson.loads


class DaysToHireStatisticsOutSchema(BaseOutSchema):
    standard_job_id: str
    country_code: Optional[str] = Field(default=None, alias="countryCode")
    avg: str = Field(default=..., alias="average")
    min: str = Field(default=..., alias="min")
    max: str = Field(default=..., alias="max")
    number_of_job_posts: int = Field(default=..., alias="numberOfJobPosts")
