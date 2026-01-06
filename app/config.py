from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    my_db_password: str
    my_db_host: str
    my_db_port: str
    my_db_name: str
    my_db_user: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()
