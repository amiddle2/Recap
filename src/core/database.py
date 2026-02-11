from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


def init_db(db_path):
    DATABASE_URL = f"sqlite:///{db_path}"

    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    return SessionLocal
