from sqlalchemy.orm import DeclarativeMeta, Mapped, mapped_column


class Categories(DeclarativeMeta):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


