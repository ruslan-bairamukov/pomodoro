from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class UserProfile(Base):
    __tablename__ = "user_profile"

    username: Mapped[str] = mapped_column(
        nullable=True, unique=True
    )
    hashed_password: Mapped[str | None]
    google_access_token: Mapped[str | None]
    yandex_access_token: Mapped[str | None]
    email: Mapped[str | None]
    name: Mapped[str | None]
