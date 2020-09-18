from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

Base = declarative_base()


class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, nullable=True)
    device_id = Column(String, nullable=True)
    app_version = Column(String, nullable=True)

    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    when = Column(String, nullable=False)
    ravings = Column(String, nullable=True)
    movie_id = Column(Integer, nullable=True)
    movie_name = Column(String, nullable=True)
    movie_poster_url = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return "<Answer(id='{}', question='{}')>" \
            .format(self.id, self.question)
