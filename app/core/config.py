from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MailGen Application"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = Field(alias="database_uri")
    SMTP_SERVER: str = Field(alias="mail_server")
    SMTP_PORT: int = Field(alias="mail_port")
    SMTP_EMAIL: str = Field(alias="mail_username")
    SMTP_PASSWORD: str = Field(alias="mail_password")
    GPT_KEY: str = Field(alias="gpt_key")
    Access_Token: str = Field(alias="access_token")
    Facebook_URL: str = "https://graph.facebook.com/v23.0"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        populate_by_name = True

settings = Settings()

