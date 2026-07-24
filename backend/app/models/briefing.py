from datetime import datetime
from sqlmodel import SQLModel,Field 

class Briefing(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: str
    level: str
    lang: str
    content: str
    generated_at: datetime = Field(default_factory=datetime.now)

    