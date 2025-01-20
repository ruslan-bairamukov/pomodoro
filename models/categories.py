from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Categories(Base):
    __tablename__ = "categories"

    name: Mapped[str]


