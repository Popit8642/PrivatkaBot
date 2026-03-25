from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    admin: Mapped[bool] = mapped_column(default=False)
    subscription_active: Mapped[bool] = mapped_column(default=False)