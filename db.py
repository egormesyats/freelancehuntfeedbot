from peewee import *
from constants import DB_NAME
db = SqliteDatabase(DB_NAME)

class BaseModel(Model):
  class Meta:
    database = db

class User(BaseModel):
  id = IntegerField(primary_key=True)
  latest_project_id = IntegerField(default=0)
  
class Skill(BaseModel):
  id = IntegerField(primary_key=True)
  name = CharField()

def launch():
  with db:
    db.create_tables([User, Skill])