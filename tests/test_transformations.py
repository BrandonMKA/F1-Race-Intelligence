import pandas as pd

from pipeline.transform.transform_laps import (
    timedelta_to_milliseconds,
)


def test_timedelta_to_milliseconds() -> None:
    values = pd.Series(
        pd.to_timedelta(
            [
                "00:01:30.500",
                "00:01:31.250",
            ]
        )
    )

    result = timedelta_to_milliseconds(values)

    assert result.tolist() == [
        90500,
        91250,
    ]


def test_timedelta_handles_missing_values() -> None:
    values = pd.Series(
        pd.to_timedelta(
            [
                "00:01:30.500",
                None,
            ]
        )
    )

    result = timedelta_to_milliseconds(values)

    assert result.iloc[0] == 90500
    assert pd.isna(result.iloc[1])
