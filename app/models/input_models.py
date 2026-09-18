from pydantic import BaseModel, Field
from typing import Optional


class EnvironmentalInput(BaseModel):

    location_id: str = Field(
        ...,
        description="Unique identifier for the assessment location"
    )

    latitude: Optional[float] = Field(
        default=None,
        description="Latitude of the location"
    )

    longitude: Optional[float] = Field(
        default=None,
        description="Longitude of the location"
    )

    soil_ph: float = Field(
        ...,
        description="Soil pH value"
    )

    soil_organic_carbon: float = Field(
        ...,
        description="Soil organic carbon measurement"
    )

    soil_moisture: float = Field(
        ...,
        description="Soil moisture measurement"
    )

    temperature: float = Field(
        ...,
        description="Temperature in degrees Celsius"
    )

    rainfall: float = Field(
        ...,
        description="Rainfall measurement"
    )

    land_use: str = Field(
        ...,
        description="Current land use category"
    )

    tree_cover_percent: float = Field(
        ...,
        ge=0,
        le=100,
        description="Tree cover percentage"
    )

    species_richness: str = Field(
        ...,
        description="Species richness category"
    )

    habitat_diversity: str = Field(
        ...,
        description="Habitat diversity category"
    )

    pollution_level: str = Field(
        ...,
        description="Pollution level"
    )

    deforestation_level: str = Field(
        ...,
        description="Deforestation level"
    )

if __name__ == "__main__":

    sample = EnvironmentalInput(
        location_id="CUSTOM001",
        latitude=21.1458,
        longitude=79.0882,
        soil_ph=6.1,
        soil_organic_carbon=0.4,
        soil_moisture=11,
        temperature=35,
        rainfall=700,
        land_use="monoculture",
        tree_cover_percent=8,
        species_richness="low",
        habitat_diversity="low",
        pollution_level="medium",
        deforestation_level="medium"
    )

    print("\nEnvironmental Input Model Test")
    print("==============================")

    print("\nValidated input:")

    print(
        sample.model_dump()
    )    