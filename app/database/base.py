from sqlalchemy.ext.declarative import declarative_base 
Base = declarative_base()


# Delay the import of User until runtime
def init_models():
    from app.database.models.user_models import User,RevokedToken # Import here to avoid circular import
    