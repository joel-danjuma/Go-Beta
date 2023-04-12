from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas, crud, oauth2, utils
from typing import List

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.post("/create", status_code = status.HTTP_201_CREATED, response_model=schemas.Admin)
def create_admin(admin: schemas.CreateAdmin, db: Session = Depends(get_db)):
    admin.password = utils.hash(admin.password)
    admin = crud.get_provider_by_email(provider.email, db)
    if db_provider:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user already exists")
    new_provider = crud.create_provider(provider,db)
    return new_provider
