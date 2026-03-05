
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

print("Database reset completed! All tables recreated.")