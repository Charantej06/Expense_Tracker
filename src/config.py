from pydantic_settings import SettingsConfigDict,BaseSettings

class settings(BaseSettings):
    DATABASE_URL : str
    JWT_SECRET : str
    JWT_ALGORITHM : str

    model_config = SettingsConfigDict(env_file='.env',extra='ignore')

config = settings()    