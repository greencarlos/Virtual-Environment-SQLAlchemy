from typing import List, Optional
from sqlalchemy import create_engine, String, select, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship

engine = create_engine("mysql+mysqlconnector://root:pa$$w0rd!@localhost/intro_orm")
session = Session(engine)


class Base(DeclarativeBase):
    pass


user_pet = Table(
    "user_pet",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("pet_id", ForeignKey("pets.id")),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(200), unique=True)

    pets: Mapped[List["Pet"]] = relationship(
        "Pet", back_populates="owner", cascade="all, delete-orphan"
    )


class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    animal: Mapped[str] = mapped_column(String(200))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship("User", back_populates="pets")


Base.metadata.create_all(engine)


dylan = User(id="100", name="Dylan", email="dkatina@email.com")
grace = User(id="200", name="Grace", email="gkat@email.com")

rhia = Pet(id="100", name="Rhiannon", animal="dog", user_id="100")
leafy = Pet(id="200", name="Leafy", animal="Chia Pet", user_id="200")

session.add_all([dylan, grace, rhia, leafy])
session.commit()

dylan = session.get(User, 100)
grace = session.get(User, 200)

rhia = session.get(Pet, 100)
leafy = session.get(Pet, 200)

dylan.pets.append(rhia)
grace.pets.append(leafy)

rhia.owner = dylan
leafy.owner = grace
session.commit()

print(dylan.pets)
