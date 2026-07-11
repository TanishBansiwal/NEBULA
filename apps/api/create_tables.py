from app.core.database import Base, engine

# Import models so SQLAlchemy knows about them
from app.models import User
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Done!")