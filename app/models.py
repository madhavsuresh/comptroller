from app import Base
from sqlalchemy import Column,Integer,DateTime,String,Text
import constants


class Presenters(Base):
    id = Column(Integer,primary_key=True)
    name = Column(String(constants.MAX_NAME))
    email = Column(String(constants.MAX_EMAIL))
    institution = Column(String(constants.MAX_INSTITUTION))
    major = Column(String(constants.MAX_MAJOR))
    year = Column(Integer())
    title = Column(Integer(constants.MAX_TITLE))
    discipline = Column(String())
    abstract = Column(Text())

