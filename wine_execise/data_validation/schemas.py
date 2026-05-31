from pydantic import BaseModel, field_validator
from typing import Optional
import pandera as pa
from pandera.typing import DataFrame, Series


# TODO: Define Pydantic model for Wine record
# class WineRecord(BaseModel):
#     alcohol: float
#     malic_acid: float
#     ash: float
#     alcalinity_of_ash: float
#     magnesium: float
#     total_phenols: float
#     flavanoids: float
#     nonflavanoid_phenols: float
#     proanthocyanins: float
#     color_intensity: float
#     hue: float
#     od280_od315: float
#     proline: float
#     class_: int  # 0=cultivar_1, 1=cultivar_2, 2=cultivar_3
#
#     @field_validator('alcohol')
#     def validate_alcohol(cls, v):
#         if v <= 0 or v > 20:
#             raise ValueError('Alcohol must be positive and realistic')
#         return v
#
#     # TODO: Add validators for other fields


# TODO: Define Pandera DataFrame schema for Wine
# WineSchema = pa.DataFrameSchema({
#     "alcohol": pa.Column(pa.Float, checks=pa.Check.greater_than(0)),
#     "malic_acid": pa.Column(pa.Float, checks=pa.Check.greater_than(0)),
#     "ash": pa.Column(pa.Float, checks=pa.Check.greater_than(0)),
#     "alcalinity_of_ash": pa.Column(pa.Float, checks=pa.Check.greater_than(0)),
#     "magnesium": pa.Column(pa.Float, checks=pa.Check.greater_than(0)),
#     "total_phenols": pa.Column(pa.Float, checks=pa.Check.greater_than(0)),
#     "flavanoids": pa.Column(pa.Float, checks=pa.Check.greater_than(0)),
#     "nonflavanoid_phenols": pa.Column(pa.Float, checks=pa.Check.greater_than(0)),
#     "proanthocyanins": pa.Column(pa.Float, checks=pa.Check.greater_than(0)),
#     "color_intensity": pa.Column(pa.Float, checks=pa.Check.greater_than(0)),
#     "hue": pa.Column(pa.Float, checks=pa.Check.greater_than(0)),
#     "od280_od315": pa.Column(pa.Float, checks=pa.Check.greater_than(0)),
#     "proline": pa.Column(pa.Float, checks=pa.Check.greater_than(0)),
#     "class": pa.Column(pa.Int, checks=pa.Check.isin([0, 1, 2])),
# })
