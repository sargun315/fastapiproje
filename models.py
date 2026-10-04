from sqlalchemy import Column,Integer,Text, String
from database import Base


#blog table
class Blog(Base):
    __tablename__="blog"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    content = Column(Text)