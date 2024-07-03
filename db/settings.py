from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from starlette.config import Config
from datetime import timedelta
from db.db import get_session

try:
    config: Config = Config(".env")
except FileNotFoundError as error:
    print(error)
    

db: str = config("DATABASE_URL", cast = str)
algorithem: str = config("ALGORITHEM", cast = str)
secret_key: str = config("SECRET_KEY", cast = str)
access_token: timedelta = timedelta(days=int(config("ACCESS_TOKEN", cast = int)))
boot_strap_server: str = config("BOOTSTRAP_SERVER", cast = str)
kafka_user_topic: str = config("KAFKA_USER_TOPIC", cast = str)
kafka_consumer_group_id: str = config("KAFKA_CONSUMER_GROUP_ID_FOR_USER", cast = str)

DB_SESSION = Annotated[Session, Depends(get_session)]