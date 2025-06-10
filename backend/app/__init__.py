import sys

from app.core.database import Base, engine
from app.models import user  # Import tất cả models cần thiết

Base.metadata.create_all(bind=engine)
