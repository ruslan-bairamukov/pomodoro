from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import settings


class DatabaseHelper:
    def __init__(
        self, url: str, echo: bool = False
    ) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,  # why?
            autocommit=False,  # why?
            expire_on_commit=False,  # why?: docs: "It’s also usually a good idea to set Session.expire_on_commit to False so that subsequent access to objects that came from a Session within the view layer do not need to emit new SQL queries to refresh the objects, if the transaction has been committed already."
        )

    async def get_db_session(
        self,
    ) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=settings.PSQL_DB.url,
    echo=settings.PSQL_DB.PSQL_ECHO,
)


"""
A scoped_session is constructed by calling it, passing it a factory which can create new Session objects. A factory is just something that produces a new object when called, and in the case of Session, the most common factory is the sessionmaker, introduced earlier in this section. Below we illustrate this usage:

>>> from sqlalchemy.orm import scoped_session
>>> from sqlalchemy.orm import sessionmaker

>>> session_factory = sessionmaker(bind=some_engine)
>>> Session = scoped_session(session_factory)

The scoped_session object we’ve created will now call upon the sessionmaker when we “call” the registry:

>>> some_session = Session()

Above, some_session is an instance of Session, which we can now use to talk to the database. This same Session is also present within the scoped_session registry we’ve created. If we call upon the registry a second time, we get back the same Session:

>>> some_other_session = Session()
>>> some_session is some_other_session
True

This pattern allows disparate sections of the application to call upon a global scoped_session, so that all those areas may share the same session without the need to pass it explicitly. The Session we’ve established in our registry will remain, until we explicitly tell our registry to dispose of it, by calling scoped_session.remove():

>>> Session.remove()

The scoped_session.remove() method first calls Session.close() on the current Session, which has the effect of releasing any connection/transactional resources owned by the Session first, then discarding the Session itself. “Releasing” here means that connections are returned to their connection pool and any transactional state is rolled back, ultimately using the rollback() method of the underlying DBAPI connection.

At this point, the scoped_session object is “empty”, and will create a new Session when called again. As illustrated below, this is not the same Session we had before:

>>> new_session = Session()
>>> new_session is some_session
False

The above series of steps illustrates the idea of the “registry” pattern in a nutshell. With that basic idea in hand, we can discuss some of the details of how this pattern proceeds.
"""
