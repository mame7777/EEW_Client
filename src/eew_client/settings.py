from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    axis_access_token: str = ""
    axis_server_list_api_url: str = ""
    axis_token_refresh_api_url: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
