import json
from aiokafka import AIOKafkaProducer # type: ignore
from auth_controllers.user_controller import create_users_in_db
from fastapi import HTTPException
from models.user_models import User, UserREQ
from security.strictnes import (hash_password, phone_number_strict, strict_email_methods, strict_first_name, strict_last_name, strict_username_methods, strong_password)
from sqlmodel import select
from db.settings import DB_SESSION, boot_strap_server, kafka_user_topic



async def create_users_in_kafka(user_for_kafka: UserREQ, db: DB_SESSION):
    is_email_exists: User | None = db.exec(select(User).where(User.email == user_for_kafka.email)).first()
    
    is_username_exists: User | None = db.exec(select(User).where(User.username == user_for_kafka.username)).first()
    
    is_phone_exists: User | None = db.exec(select(User).where(User.phone_number == user_for_kafka.phone_number)).first()
    
    
    if is_email_exists:
        raise HTTPException(status_code=400, detail="This Email is already exists")
    elif is_username_exists:
        raise HTTPException(status_code=400, detail="This Username is already exists")
    elif is_phone_exists:
        raise HTTPException(status_code=400, detail="This Phone Number is already exists")
    elif is_email_exists and is_username_exists:
        raise HTTPException(status_code=400, detail="This Email and Username is already in use")
    
    if not strict_first_name(user_for_kafka.first_name):
        raise HTTPException(status_code=400, detail="Your First Name is not valid")
    
    if not strict_last_name(user_for_kafka.last_name):
        raise HTTPException(status_code=400, detail="Your Last Name is not valid")
    
    if not strict_username_methods(user_for_kafka.username):
        raise HTTPException(status_code=400, detail="Your Username is not valid")
        
    if not strict_email_methods(user_for_kafka.email):
        raise HTTPException(status_code=400, detail="Your Email is not valid")
    
    if not strong_password(user_for_kafka.password):
        raise HTTPException(status_code=400, detail="Your password is not strong enough please recreate your password and your password must be in (upper, lower, number, special characters)")
    
    if not phone_number_strict(user_for_kafka.phone_number):
        
        raise HTTPException(status_code=400, detail="please use only pakistani number")
    user_for_kafka.password = hash_password(user_for_kafka.password)
    producer = AIOKafkaProducer(bootstrap_servers = boot_strap_server)
    create_user_producer = json.dumps(user_for_kafka.__dict__).encode("utf-8")
    await producer.start()
    try:
        await producer.send_and_wait(kafka_user_topic, create_user_producer) 
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Failed to create user: {error}")
    else:
        try:
            users = await create_users_in_db(user = user_for_kafka, db = db)
            return users
        except:
            raise HTTPException(status_code=400, detail="Failed to create user in database")
    finally:
        await producer.stop()