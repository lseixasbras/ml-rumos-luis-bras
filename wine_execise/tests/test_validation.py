import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

# TODO: Import your schemas here
# from data_validation.schemas import WineRecord, WineSchema


# TODO: Write tests here
# def test_wine_record_negative_alcohol():
#     try:
#         WineRecord(alcohol=-1, malic_acid=1.0, ash=2.0, alcalinity_of_ash=15.0,
#                    magnesium=100, total_phenols=2.0, flavanoids=2.0,
#                    nonflavanoid_phenols=0.3, proanthocyanins=1.5,
#                    color_intensity=5.0, hue=1.0, od280_od315=3.0,
#                    proline=1000, class_=0)
#         assert False, "Should raise ValueError"
#     except ValueError:
#         pass


# def test_wine_record_valid():
#     record = WineRecord(alcohol=14.23, malic_acid=1.71, ash=2.43,
#                         alcalinity_of_ash=15.6, magnesium=127,
#                         total_phenols=2.8, flavanoids=3.06,
#                         nonflavanoid_phenols=0.28, proanthocyanins=2.29,
#                         color_intensity=5.64, hue=1.04, od280_od315=3.92,
#                         proline=1065, class_=0)
#     assert record.alcohol == 14.23


# TODO: Add more tests for:
# - Invalid class values (not 0, 1, or 2)
# - Invalid feature measurements (negative values, unrealistic ranges)
# - Pandera schema validation
