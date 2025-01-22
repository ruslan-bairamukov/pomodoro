from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class UserProfile(Base):
    __tablename__ = "user_profile"

    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    access_token: Mapped[str] = mapped_column(
        nullable=False
    )
