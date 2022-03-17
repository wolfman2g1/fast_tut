from pydantic import BaseSettings


""" would set this up later to get the settings"""
class Settings(BaseSettings):
    database_host: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algo : str
    access_token_expire_mins: int


settings = Settings()