from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

class EmailLookupRequest(BaseModel):
    email: EmailStr

class MetaDataResponse(BaseModel):
    facebook_page: Optional[Dict[str, Any]]
    instagram_account: Optional[Dict[str, Any]]
