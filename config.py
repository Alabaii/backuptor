from pydantic import BaseSettings

class Settings(BaseSettings):

    #database mariadb
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    #ssh 
    SSH_HOST: str
    SSH_USER: str
    SSH_PASS: str
    SSH_PORT: int

    
    class Config:
        env_file=".env"

settings = Settings()