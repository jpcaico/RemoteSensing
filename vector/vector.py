import fiona
from pydantic import BaseModel, Field, field_validator
from typing import List, Tuple

# --- 1. The Pydantic Model ---
class PopulatedPlace(BaseModel):
    name: str
    population: int = Field(alias="POP_MAX")
    # Store as a simple tuple (lon, lat) for the "think in Python" test
    coordinates: Tuple[float, float]

    @field_validator('population')
    @classmethod
    def must_be_positive(cls, v: int) -> int:
        if v < 0:
            return 0  # Data cleaning logic
        return v

# --- 2. The OOP Processor ---
class SpatialDataIngestor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def stream_features(self, limit: int = 10):
        """A generator that yields validated Pydantic models"""
        try:
            with fiona.open(self.file_path, 'r') as source:
                for i, feature in enumerate(source):
                    if i >= limit:
                        break
                    
                    # Mapping the 'raw' record to our Pydantic model
                    yield PopulatedPlace(
                        name=feature['properties']['NAME'],
                        POP_MAX=feature['properties']['POP_MAX'],
                        coordinates=feature['geometry']['coordinates']
                    )
        except FileNotFoundError:
            print(f"Error: Path {self.file_path} does not exist.")
        except Exception as e:
            print(f"Ingestion failed: {e}")

# --- 3. Execution ---
if __name__ == "__main__":
    ingestor = SpatialDataIngestor('data/ne_50m_populated_places.shp')
    
    for place in ingestor.stream_features(limit=5):
        print(f"City: {place.name} | Pop: {place.population} | Coords: {place.coordinates}")