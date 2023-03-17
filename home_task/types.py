import uuid


class StrUUID(str):
    @classmethod
    def __get_validators__(cls):
        """Run validate class method."""
        yield cls.validate

    @classmethod
    def validate(cls, v) -> str:
        """Validate UUID object and convert it to string."""
        if isinstance(v, uuid.UUID):
            return str(v)

        try:
            result = uuid.UUID(v)
        except ValueError as error:
            raise ValueError("Invalid UUID") from error
        else:
            return str(result)
