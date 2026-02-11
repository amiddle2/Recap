import sqlalchemy as db

from src.core.database import Base


class Questions(Base):
    __tablename__ = "questions"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    question = db.Column(db.String(), nullable=False)
    correct_answer = db.Column(db.String(), nullable=False)
