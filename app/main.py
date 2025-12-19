from __future__ import annotations

from datetime import date, timedelta
from io import BytesIO
from typing import Literal, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response

app = FastAPI(title="EduTrack API")


AttendanceInterval = Literal["daily", "monthly", "yearly"]


def build_sample_attendance_dataset() -> pd.DataFrame:
    """Create sample attendance data for reporting purposes.

    The dataset is intentionally deterministic so that reports are predictable
    without a backing database.
    """

    today = date.today()
    records = []
    for day_offset in range(0, 60):
        current_day = today - timedelta(days=day_offset)
        for grade in ("1", "2", "3", "4"):  # simple sample grades
            for section in ("A", "B"):
                # Create pseudo attendance figures that fluctuate over time.
                present = max(18, 28 - (day_offset % 7) - (int(grade) - 1))
                enrolled = 30
                absent = max(0, enrolled - present)
                records.append(
                    {
                        "date": current_day,
                        "grade": grade,
                        "section": section,
                        "present": present,
                        "absent": absent,
                        "enrolled": enrolled,
                    }
                )

    df = pd.DataFrame.from_records(records)
    df["date"] = pd.to_datetime(df["date"])
    return df


def filter_dataset(
    df: pd.DataFrame, grade: Optional[str], section: Optional[str]
) -> pd.DataFrame:
    """Filter the dataset by grade and section when they are provided."""

    filtered = df.copy()

    if grade:
        filtered = filtered[filtered["grade"].str.lower() == grade.lower()]

    if section:
        filtered = filtered[filtered["section"].str.lower() == section.lower()]

    return filtered


def summarize_attendance(
    df: pd.DataFrame, interval: AttendanceInterval
) -> pd.DataFrame:
    """Aggregate attendance depending on the requested interval."""

    if df.empty:
        raise HTTPException(status_code=404, detail="No attendance data for the selection.")

    if interval == "daily":
        grouped = (
            df.groupby(["date", "grade", "section"], as_index=False)[["present", "absent", "enrolled"]]
            .sum()
            .rename(columns={"date": "period"})
        )
    elif interval == "monthly":
        df["period"] = df["date"].dt.to_period("M").dt.to_timestamp()
        grouped = (
            df.groupby(["period", "grade", "section"], as_index=False)[["present", "absent", "enrolled"]]
            .sum()
        )
    else:  # yearly
        df["period"] = df["date"].dt.to_period("Y").dt.to_timestamp()
        grouped = (
            df.groupby(["period", "grade", "section"], as_index=False)[["present", "absent", "enrolled"]]
            .sum()
        )

    grouped = grouped.sort_values(["period", "grade", "section"]).reset_index(drop=True)
    grouped["attendance_rate"] = (grouped["present"] / grouped["enrolled"]).round(3)
    return grouped


def dataframe_to_excel_bytes(df: pd.DataFrame) -> bytes:
    """Convert a DataFrame to Excel bytes using openpyxl."""

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Attendance")
    buffer.seek(0)
    return buffer.read()


@app.get("/api/reports/attendance.xlsx")
async def export_attendance_report(
    interval: AttendanceInterval = Query(
        ..., description="Aggregation interval for the report", alias="period"
    ),
    grade: Optional[str] = Query(None, description="Grade to filter the report"),
    section: Optional[str] = Query(None, description="Section to filter the report"),
):
    """Export an attendance report to Excel.

    Query parameters
    ----------------
    period: ``daily`` | ``monthly`` | ``yearly``
    grade: optional grade filter
    section: optional section filter
    """

    dataset = build_sample_attendance_dataset()
    filtered = filter_dataset(dataset, grade=grade, section=section)
    summary = summarize_attendance(filtered, interval=interval)

    excel_bytes = dataframe_to_excel_bytes(summary)

    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=attendance.xlsx"},
    )
