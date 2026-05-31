import pandas as pd
import pandera.pandas as pa
from config import get_logger
from data_validation.schemas import WineRecord, WineSchema

logger = get_logger(__name__)

REQUIRED_COLS = list(WineSchema.columns.keys())


def validate_with_pydantic(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Validate each row of a DataFrame against the Pydantic WineRecord model.

    Args:
        df: DataFrame to validate.

    Returns:
        Tuple: (valid DataFrame, invalid DataFrame with _validation_error column).
    """
    valid_rows = []
    invalid_rows = []

    for _, row in df.iterrows():
        row_dict = row.to_dict()
        if "class" in row_dict:
            row_dict["class_"] = row_dict.pop("class")
        try:
            WineRecord(**row_dict)
            valid_rows.append(row)
        except Exception as e:
            row_with_error = row.to_dict()
            row_with_error["_validation_error"] = str(e)
            invalid_rows.append(row_with_error)

    valid_df = pd.DataFrame(valid_rows) if valid_rows else pd.DataFrame(columns=df.columns)
    invalid_df = pd.DataFrame(invalid_rows) if invalid_rows else pd.DataFrame()

    logger.info(f"Pydantic validation: {len(valid_df)} valid, {len(invalid_df)} invalid (out of {len(df)})")
    return valid_df, invalid_df


def validate_with_pandera(df: pd.DataFrame) -> tuple[bool, str | None]:
    """
    Validate a DataFrame against the Pandera WineSchema.

    Args:
        df: DataFrame to validate.

    Returns:
        Tuple: (bool success, error message or None).
    """
    try:
        WineSchema.validate(df, lazy=True)
        logger.info("Pandera validation: PASSED")
        return True, None
    except pa.errors.SchemaErrors as e:
        logger.warning(f"Pandera validation: FAILED ({e})")
        return False, str(e)
    except Exception as e:
        logger.error(f"Pandera validation error: {e}")
        return False, str(e)
