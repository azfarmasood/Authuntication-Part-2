from aiokafka import AIOKafkaConsumer # type: ignore
from fastapi import FastAPI
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine
from db.settings import db, kafka_consumer_group_id, kafka_user_topic, boot_strap_server
import asyncio


connection_string: str = str(db).replace("postgresql", "postgresql+psycopg")

engine: Engine = create_engine(connection_string, pool_pre_ping = True, echo = True, pool_recycle = 300, max_overflow = 0)


async def get_kafka_consumer(topic: str, boot_strap_servers: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers = boot_strap_servers,
        group_id = kafka_consumer_group_id,
        auto_offset_reset='earliest'
        )
    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received This Message From {message.partition} And Received This From {message.topic}")
            print(f"Received User Data: {message.value.decode()} From This {message.topic}")
            print(f"Created at: {message.timestamp}")
    finally:
        await consumer.stop()


async def create_tables(app:FastAPI):
    print(f"create_tables...{app}")
    task = asyncio.create_task(get_kafka_consumer(topic = kafka_user_topic, boot_strap_servers = boot_strap_server))
    SQLModel.metadata.create_all(bind = engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session