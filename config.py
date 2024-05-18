from typing import Tuple, Type

from pydantic import BaseModel, IPvAnyAddress, field_validator
from pydantic_settings import (BaseSettings, PydanticBaseSettingsSource,
                               SettingsConfigDict, YamlConfigSettingsSource)


class Sensor(BaseModel):
    """
    传感器配置
    """
    ip: IPvAnyAddress
    campus: str
    building: str
    room: str | int

    @field_validator("room")
    @classmethod
    def convert_room(cls, v):
        """
        Convert room to string
        """
        return str(v)

    @field_validator("ip")
    @classmethod
    def convert_ip(cls, v):
        """
        Convert ip to string
        """
        return str(v)


class Settings(BaseSettings):
    sensors: list[Sensor] = []
    model_config = SettingsConfigDict(yaml_file="config.yaml")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)


settings = Settings()


if __name__ == "__main__":
    settings = Settings()
    print(settings.sensors)
    print(settings.model_config)
    print(settings.model_dump())
