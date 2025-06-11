from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserInDB, CustomerBase, UserLogin, Token, CustomerBase, RegisterRequest
from app.crud import user as crud_user
from app.deps.deps import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login/", response_model=Token)
# Loại bỏ = Depends() ở đây để nhận JSON body trực tiếp
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    token_data = crud_user.login_for_access_token(user_login, db)
    # Vì login_for_access_token đã raise HTTPException nếu lỗi,
    # nếu đến được đây tức là thành công
    return token_data


@router.get("/customers/", response_model=list[CustomerBase])
def read_users(db: Session = Depends(get_db)):
    return crud_user.get_users(db)


@router.get("/customer/me/", response_model=CustomerBase)
def read_customer_me(db: Session = Depends(get_db), token: str= Depends(oauth2_scheme)):
    current_user = crud_user.get_current_user(db, token)
    return current_user

@router.post("/register/")
def register(user: RegisterRequest, db: Session = Depends(get_db)):
    crud_user.create_user(db, user)


# @router.get("/users", response_model=list[UserOut])
# def read_users(db: Session = Depends(get_db)):
#     return crud_user.get_users(db)

# @router.get("/users/{user_id}", response_model=UserOut)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud_user.get_user_by_id(db, user_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# @router.post("/users", response_model=UserOut)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     return crud_user.create_user(db, user)


# @app.post("/users/", response_model=schemas.UserInDB, status_code=status.HTTP_201_CREATED)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     # Check if UserID already exists (assuming UserID is NOT SERIAL in DB)
#     # If UserID is SERIAL (auto-increment), remove UserID from UserCreate and let DB handle it
#     # And allow UserID to be auto-generated in models.py (e.g., UserID = Column(Integer, primary_key=True, autoincrement=True))
#     existing_user = db.query(models.User).filter(models.User.UserID == user.UserID).first()
#     if existing_user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="UserID already registered")

#     # Check if Username already exists
#     existing_username = db.query(models.User).filter(models.User.Username == user.Username).first()
#     if existing_username:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

#     db_user = models.User(
#         UserID=user.UserID,
#         Username=user.Username,
#         PasswordHash=user.PasswordHash,
#         Email=user.Email
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user



# @app.get("/users/{user_id}", response_model=schemas.UserInDB)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.UserID == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     return user

# @app.put("/users/{user_id}", response_model=schemas.UserInDB)
# def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
#     db_user = db.query(models.User).filter(models.User.UserID == user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     # Update fields that are provided
#     update_data = user_update.model_dump(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_user, key, value)

#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = db.query(models.User).filter(models.User.UserID == user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     db.delete(db_user)
#     db.commit()
#     # No content returned for 204 status
#     return {}

# # --- CUSTOMER Endpoints ---

# @app.post("/customers/", response_model=schemas.CustomerInDB, status_code=status.HTTP_201_CREATED)
# def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
#     # Check if UserID exists in Users table
#     user_exists = db.query(models.User).filter(models.User.UserID == customer.UserID).first()
#     if not user_exists:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="UserID not found in Users table")

#     # Check if a customer record already exists for this UserID
#     existing_customer = db.query(models.Customer).filter(models.Customer.UserID == customer.UserID).first()
#     if existing_customer:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Customer with UserID {customer.UserID} already exists")

#     db_customer = models.Customer(
#         UserID=customer.UserID,
#         FullName=customer.FullName,
#         Address=customer.Address,
#         PhoneNumber=customer.PhoneNumber,
#         BirthDate=customer.BirthDate
#     )
#     db.add(db_customer)
#     db.commit()
#     db.refresh(db_customer)
#     return db_customer

# @app.get("/customers/", response_model=List[schemas.CustomerInDB])
# def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     customers = db.query(models.Customer).offset(skip).limit(limit).all()
#     return customers

# @app.get("/customers/{user_id}", response_model=schemas.CustomerInDB)
# def read_customer(user_id: int, db: Session = Depends(get_db)):
#     customer = db.query(models.Customer).filter(models.Customer.UserID == user_id).first()
#     if customer is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found for this UserID")
#     return customer

# @app.put("/customers/{user_id}", response_model=schemas.CustomerInDB)
# def update_customer(user_id: int, customer_update: schemas.CustomerUpdate, db: Session = Depends(get_db)):
#     db_customer = db.query(models.Customer).filter(models.Customer.UserID == user_id).first()
#     if db_customer is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found for this UserID")

#     update_data = customer_update.model_dump(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_customer, key, value)

#     db.add(db_customer)
#     db.commit()
#     db.refresh(db_customer)
#     return db_customer

# @app.delete("/customers/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_customer(user_id: int, db: Session = Depends(get_db)):
#     db_customer = db.query(models.Customer).filter(models.Customer.UserID == user_id).first()
#     if db_customer is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found for this UserID")

#     db.delete(db_customer)
#     db.commit()
#     return {}

# # --- ADMIN Endpoints ---

# @app.post("/admins/", response_model=schemas.AdminInDB, status_code=status.HTTP_201_CREATED)
# def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
#     # Check if UserID exists in Users table
#     user_exists = db.query(models.User).filter(models.User.UserID == admin.UserID).first()
#     if not user_exists:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="UserID not found in Users table")

#     # Check if an admin record already exists for this UserID
#     existing_admin = db.query(models.Admin).filter(models.Admin.UserID == admin.UserID).first()
#     if existing_admin:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Admin with UserID {admin.UserID} already exists")

#     db_admin = models.Admin(
#         UserID=admin.UserID,
#         PhoneNumber=admin.PhoneNumber
#     )
#     db.add(db_admin)
#     db.commit()
#     db.refresh(db_admin)
#     return db_admin

# @app.get("/admins/", response_model=List[schemas.AdminInDB])
# def read_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     admins = db.query(models.Admin).offset(skip).limit(limit).all()
#     return admins

# @app.get("/admins/{user_id}", response_model=schemas.AdminInDB)
# def read_admin(user_id: int, db: Session = Depends(get_db)):
#     admin = db.query(models.Admin).filter(models.Admin.UserID == user_id).first()
#     if admin is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found for this UserID")
#     return admin

# @app.put("/admins/{user_id}", response_model=schemas.AdminInDB)
# def update_admin(user_id: int, admin_update: schemas.AdminUpdate, db: Session = Depends(get_db)):
#     db_admin = db.query(models.Admin).filter(models.Admin.UserID == user_id).first()
#     if db_admin is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found for this UserID")

#     update_data = admin_update.model_dump(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_admin, key, value)

#     db.add(db_admin)
#     db.commit()
#     db.refresh(db_admin)
#     return db_admin

# @app.delete("/admins/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_admin(user_id: int, db: Session = Depends(get_db)):
#     db_admin = db.query(models.Admin).filter(models.Admin.UserID == user_id).first()
#     if db_admin is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found for this UserID")

#     db.delete(db_admin)
#     db.commit()
#     return {}