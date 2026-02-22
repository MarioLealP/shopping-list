from settings import settings
from datetime import datetime
import uuid
from sqlmodel import SQLModel, Field, create_engine

engine = create_engine(settings.database_url)

class BaseDatabaseModel(SQLModel):
	pass

class Note(BaseDatabaseModel, table=True):
	id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
	title: str
	content: str
	create_date: datetime
	modified_date: datetime