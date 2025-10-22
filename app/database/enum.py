import enum
from sqlalchemy.dialects.postgresql import ENUM
# Define Role Enum
class RoleEnum(enum.Enum):
    admin = "admin"
    user = "user"

