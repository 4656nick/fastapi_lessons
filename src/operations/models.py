from datetime import datetime

from sqlalchemy import MetaData, Integer, String, Table, Column, ForeignKey, TIMESTAMP, JSON, Boolean

metadata = MetaData()

operation = Table(
    "operation",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("quantity", String),
    Column("figi", String),
    Column("instrument_type", String),
    Column("date", TIMESTAMP),
    Column("type", String)
)