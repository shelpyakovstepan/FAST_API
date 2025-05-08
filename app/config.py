from pydantic_settings import BaseSettings, SettingsConfigDict
import os

#DOTENV = os.path.join(os.path.dirname(__file__), ".env")
#abs_path_env = os.path.abspath(".env")


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str

    #model_config = SettingsConfigDict( case_sensitive=True, env_file=abs_path_env)
    class Config:
        env_file = ".env"



settings = Settings()



