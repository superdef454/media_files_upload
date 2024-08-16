from datetime import datetime

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict
from zoneinfo import ZoneInfo


def datetime_to_gmt_str(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class CustomModel(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: datetime_to_gmt_str},
        populate_by_name=True,
    )

    def serializable_dict(self, **kwargs) -> dict:  # noqa: ARG002
        """Вернёт словарь, содержащий только сериализуемые поля."""
        default_dict = self.model_dump()

        return jsonable_encoder(default_dict)
