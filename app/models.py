from app.database import Base
from sqlalchemy import Column,Integer,String,Text
import constants


class Presenters(Base):
    __tablename__ = 'presenters'
    id = Column(Integer,primary_key=True)
    reg_num = Column(String(constants.MAX_REGNUM),unique=True)
    name = Column(String(constants.MAX_NAME))
    email = Column(String(constants.MAX_EMAIL))
    institution = Column(String(constants.MAX_INSTITUTION))
    major = Column(String(constants.MAX_MAJOR))
    year = Column(Integer())
    title = Column(Integer(constants.MAX_TITLE))
    discipline = Column(String())
    abstract = Column(Text())

    def __init__(self,name=None,email=None,
                institution=None,major=None,year=None,title=None,
                abstract_title=None, discipline=None,abstract=None,
                arg_dict=None):

        if arg_dict:
            self.name = arg_dict['name']
            self.email = arg_dict['email']
            self.institution = arg_dict['institution']
            self.major = arg_dict['major']
            self.year = arg_dict['year']
            self.abstract_title = arg_dict['abstract_title']
            self.discipline = arg_dict['discipline']
            self.abstract = arg_dict['abstract']
        else:
            self.name = name
            self.email = email
            self.institution = institution
            self.major = major
            self.year = year
            self.abstract_title = abstract_title
            self.discipline = discipline
            self.abstract = abstract


