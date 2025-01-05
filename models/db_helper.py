from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from collections.abc import Generator

from config.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self) -> Session:
        session = scoped_session(
            session_factory=self.session_factory,
        )
        return session

    def session_dependency(self) -> Generator[Session, None]:
        with self.session_factory() as sess:
            yield sess
            sess.close()


db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.echo,
)
