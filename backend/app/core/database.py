from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings
from sqlalchemy.ext.automap import automap_base

engine = create_engine(settings.database_url) #đường dẫn xuống db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #bind vào engine đó để tạo ra sessionLocal
#Base = declarative_base() #lớp cơ sở (Base) định nghĩa các bảng trong cơ sở dữ liệu. 
#Các lớp con của Base sẽ được SQLAlchemy nhận diện là ORM models.

# ORM Model bao gồm
# Lớp (class) trong mã nguồn của bạn sẽ ánh xạ tới bảng trong cơ sở dữ liệu.

# Thuộc tính (attribute) của lớp tương ứng với cột (column) trong bảng.

# Instance của lớp là một đối tượng thực tế, đại diện cho một dòng (record) trong db

# Khởi tạo base model
Base = automap_base()

# Phản ánh các bảng trong cơ sở dữ liệu
Base.prepare(engine, reflect=True)

