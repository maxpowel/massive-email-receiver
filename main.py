from applauncher import Kernel, ServiceContainer
from motor_bundle import MotorBundle
from massive_mail_receiver_bundle import MassiveEmailServerBundle
import asyncio
import logging

with Kernel(bundles=[MotorBundle(), MassiveEmailServerBundle()], environment="prod") as kernel:
    loop = asyncio.get_event_loop()
    server = ServiceContainer.massive_email_receiver.server()
    config = ServiceContainer.massive_email_receiver.configuration.provided().massive_email_receiver
    logging.info("Server listening %s:%s", config.hostname, config.port)
    server.begin()
    loop.run_forever()
    kernel.wait()
