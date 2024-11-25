"""Models for fixtures."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from mashumaro.mixins.orjson import DataClassORJSONMixin
from mashumaro.mixins.yaml import DataClassYAMLMixin

from myskoda.models.info import Capability, Info


class FixtureReportType(StrEnum):
    GET = "get"


class Endpoint(StrEnum):
    INFO = "info"
    STATUS = "status"
    AIR_CONDITIONING = "air_conditioning"
    AUXILIARY_HEATING = "auxiliary_heating"
    POSITIONS = "positions"
    HEALTH = "health"
    CHARGING = "charging"
    MAINTENANCE = "maintenance"
    DRIVING_RANGE = "driving_range"
    TRIP_STATISTICS = "trip_statistics"
    ALL = "all"


@dataclass
class FixtureReportGet(DataClassYAMLMixin):
    type: FixtureReportType
    vehicle_id: int
    success: bool
    endpoint: Endpoint
    raw: str | None = field(default=None)
    url: str | None = field(default=None)
    result: dict | None = field(default=None)
    error: str | None = field(default=None)


@dataclass
class FixtureVehicle(DataClassYAMLMixin):
    id: int
    device_platform: str
    system_model_id: str
    model: str
    model_year: str
    trim_level: str | None
    software_version: str | None
    capabilities: list[Capability]


def create_fixture_vehicle(id: int, info: Info) -> FixtureVehicle:  # noqa: A002
    """Create a new `FixtureVehicle` from an info."""
    return FixtureVehicle(
        id=id,
        device_platform=info.device_platform,
        system_model_id=info.specification.system_model_id,
        capabilities=info.capabilities.capabilities,
        model=info.specification.model,
        model_year=info.specification.model_year,
        software_version=info.software_version,
        trim_level=info.specification.trim_level,
    )


@dataclass
class Fixture(DataClassORJSONMixin, DataClassYAMLMixin):
    """A fixture for a test generated by the CLI."""

    name: str
    description: str | None
    generation_time: datetime
    library_version: str
    vehicles: list[FixtureVehicle]
    reports: list[FixtureReportGet] | None
