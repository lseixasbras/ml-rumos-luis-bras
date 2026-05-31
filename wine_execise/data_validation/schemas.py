from pydantic import BaseModel, field_validator
import pandera.pandas as pa
from pandera.typing import DataFrame, Series


class WineRecord(BaseModel):
    """Pydantic model for a single wine record with domain-aware validators."""
    alcohol: float
    malic_acid: float
    ash: float
    alcalinity_of_ash: float
    magnesium: int
    total_phenols: float
    flavanoids: float
    nonflavanoid_phenols: float
    proanthocyanins: float
    color_intensity: float
    hue: float
    od280_od315: float
    proline: int
    class_: int  # 0=cultivar_1, 1=cultivar_2, 2=cultivar_3

    @field_validator('alcohol')
    @classmethod
    def validate_alcohol(cls, v):
        # Wine alcohol typically 8-17% ABV; outside this is suspect
        if v < 8 or v > 17:
            raise ValueError(f'Alcohol {v} out of realistic range [8, 17]')
        return v

    @field_validator('malic_acid')
    @classmethod
    def validate_malic_acid(cls, v):
        # Malic acid must be positive; above 7 g/L is extremely unusual
        if v < 0 or v > 7:
            raise ValueError(f'Malic acid {v} out of range [0, 7]')
        return v

    @field_validator('ash')
    @classmethod
    def validate_ash(cls, v):
        # Ash content in wine: typically 1-4 g/L
        if v < 0.5 or v > 5:
            raise ValueError(f'Ash {v} out of range [0.5, 5]')
        return v

    @field_validator('alcalinity_of_ash')
    @classmethod
    def validate_alcalinity_of_ash(cls, v):
        # Alcalinity: typically 5-35 mEq/L for wine
        if v < 5 or v > 40:
            raise ValueError(f'Alcalinity of ash {v} out of range [5, 40]')
        return v

    @field_validator('magnesium')
    @classmethod
    def validate_magnesium(cls, v):
        # Magnesium in wine: typically 50-200 mg/L
        if v < 50 or v > 200:
            raise ValueError(f'Magnesium {v} out of range [50, 200]')
        return v

    @field_validator('total_phenols')
    @classmethod
    def validate_total_phenols(cls, v):
        # Must be positive; upper bound generous for concentrated wines
        if v <= 0 or v > 6:
            raise ValueError(f'Total phenols {v} out of range (0, 6]')
        return v

    @field_validator('flavanoids')
    @classmethod
    def validate_flavanoids(cls, v):
        # Can be very low in some cultivars but not negative
        if v < 0 or v > 6:
            raise ValueError(f'Flavanoids {v} out of range [0, 6]')
        return v

    @field_validator('nonflavanoid_phenols')
    @classmethod
    def validate_nonflavanoid_phenols(cls, v):
        # Small fraction of total phenols; typically 0-1
        if v < 0 or v > 1.5:
            raise ValueError(f'Nonflavanoid phenols {v} out of range [0, 1.5]')
        return v

    @field_validator('proanthocyanins')
    @classmethod
    def validate_proanthocyanins(cls, v):
        # Tannin compounds; must be positive
        if v < 0 or v > 5:
            raise ValueError(f'Proanthocyanins {v} out of range [0, 5]')
        return v

    @field_validator('color_intensity')
    @classmethod
    def validate_color_intensity(cls, v):
        # Optical density; must be positive, can be high in concentrated reds
        if v <= 0 or v > 20:
            raise ValueError(f'Color intensity {v} out of range (0, 20]')
        return v

    @field_validator('hue')
    @classmethod
    def validate_hue(cls, v):
        # Optical density ratio; typically 0.3-2.0
        if v <= 0 or v > 2.5:
            raise ValueError(f'Hue {v} out of range (0, 2.5]')
        return v

    @field_validator('od280_od315')
    @classmethod
    def validate_od280_od315(cls, v):
        # UV absorption ratio; must be positive
        if v <= 0 or v > 5:
            raise ValueError(f'OD280/OD315 {v} out of range (0, 5]')
        return v

    @field_validator('proline')
    @classmethod
    def validate_proline(cls, v):
        # Amino acid content; typically 200-2000 mg/L in wine
        if v < 100 or v > 2500:
            raise ValueError(f'Proline {v} out of range [100, 2500]')
        return v

    @field_validator('class_')
    @classmethod
    def validate_class(cls, v):
        # Must be one of the 3 cultivar classes
        if v not in (0, 1, 2):
            raise ValueError(f'Class must be 0, 1, or 2 — got {v}')
        return v


# Pandera DataFrame schema for batch validation
WineSchema = pa.DataFrameSchema({
    "alcohol": pa.Column(float, checks=[
        pa.Check.in_range(8, 17),
    ], nullable=False),
    "malic_acid": pa.Column(float, checks=[
        pa.Check.in_range(0, 7),
    ], nullable=False),
    "ash": pa.Column(float, checks=[
        pa.Check.in_range(0.5, 5),
    ], nullable=False),
    "alcalinity_of_ash": pa.Column(float, checks=[
        pa.Check.in_range(5, 40),
    ], nullable=False),
    "magnesium": pa.Column(int, checks=[
        pa.Check.in_range(50, 200),
    ], nullable=False),
    "total_phenols": pa.Column(float, checks=[
        pa.Check.greater_than(0),
        pa.Check.less_than_or_equal_to(6),
    ], nullable=False),
    "flavanoids": pa.Column(float, checks=[
        pa.Check.greater_than_or_equal_to(0),
        pa.Check.less_than_or_equal_to(6),
    ], nullable=False),
    "nonflavanoid_phenols": pa.Column(float, checks=[
        pa.Check.in_range(0, 1.5),
    ], nullable=False),
    "proanthocyanins": pa.Column(float, checks=[
        pa.Check.in_range(0, 5),
    ], nullable=False),
    "color_intensity": pa.Column(float, checks=[
        pa.Check.greater_than(0),
        pa.Check.less_than_or_equal_to(20),
    ], nullable=False),
    "hue": pa.Column(float, checks=[
        pa.Check.greater_than(0),
        pa.Check.less_than_or_equal_to(2.5),
    ], nullable=False),
    "od280_od315": pa.Column(float, checks=[
        pa.Check.greater_than(0),
        pa.Check.less_than_or_equal_to(5),
    ], nullable=False),
    "proline": pa.Column(int, checks=[
        pa.Check.in_range(100, 2500),
    ], nullable=False),
    "class": pa.Column(int, checks=[
        pa.Check.isin([0, 1, 2]),
    ], nullable=False),
})
