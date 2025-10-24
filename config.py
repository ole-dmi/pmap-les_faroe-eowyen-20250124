import yaml
from pathlib    import Path
from pydantic   import BaseModel, ValidationError
from typing     import Literal
from typing     import Annotated
from pydantic   import BaseModel, Field

class GeoTiffConfig(BaseModel):
    input_path: Path

class NetCdfConfig(BaseModel):
    x0: float
    y0: float
    Lx: float
    Ly: float
    nx: int
    ny: int
    output_path: Path
    filename: str

class AppConfig(BaseModel):
    geotiff: Annotated[
        GeoTiffConfig | None, Field(default=None)
    ]
    netcdf: Annotated[
        NetCdfConfig | None, Field(default=None)
    ]

def load_config(path: str | Path = "config/config.yaml") -> AppConfig:
    path = Path(path)
    with path.open() as f:
        data = yaml.safe_load(f)
        
    try:
        return AppConfig(**data)
    except ValidationError as e:
        print("❌ Config validation error:")
        print(e)
        raise
