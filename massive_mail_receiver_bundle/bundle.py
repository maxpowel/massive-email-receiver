from applauncher.applauncher import Configuration
from dependency_injector import providers, containers
from pydantic import BaseModel
from aiosmtpd.controller import UnthreadedController
from motor_bundle.bundle import MotorContainer
from .mail import MongoSMTPHandler
import logging
import asyncio

logger = logging.getLogger("email")

class MailConfig(BaseModel):
    hostname: str = "localhost"
    port: int = 25
    mongo_database: str = "emails"


class MailContainer(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=MailConfig)
    configuration = Configuration()
    handler = providers.Factory(
        MongoSMTPHandler,
        database_name=configuration.provided.massive_email_receiver.mongo_database,
        mongo=MotorContainer.client
    )
    server = providers.Singleton(
        UnthreadedController,
        loop=asyncio.get_event_loop(),
        handler=handler,
        hostname=configuration.provided.massive_email_receiver.hostname,
        port=configuration.provided.massive_email_receiver.port
    )


class MassiveEmailServerBundle:
    def __init__(self):
        self.config_mapping = {
            "massive_email_receiver": MailConfig
        }

        self.injection_bindings = {
            'massive_email_receiver': MailContainer
        }
