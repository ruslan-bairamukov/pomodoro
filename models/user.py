from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class UserProfile(Base):
    __tablename__ = "user_profile"

    username: Mapped[str] = mapped_column(
        nullable=False, unique=True
    )
    hashed_password: Mapped[str] = mapped_column(
        nullable=False
    )
