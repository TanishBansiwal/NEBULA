from app.core.database import Base, engine

# Import models so SQLAlchemy knows about them
from app.models import User

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Done!")