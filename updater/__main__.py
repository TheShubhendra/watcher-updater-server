import logging
import asyncio
from watcher import Watcher
import updater.database_api as api
from decouple import config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=logging.DEBUG,
)

UPDATER_ID = config("UPDATER_ID")
logger = logging.getLogger(__name__)


class Server(Watcher):
    def start(self):
        logger.info("Starting Server")
        users = api.fetch_usernames(UPDATER_ID)
        for id, usernames in users:
            self.add_quora(usernames, update_interval=3)
        loop = asyncio.get_running_loop()
        logger.info("Creating task to run watcher")
        self.running_task = loop.create_task(self.run())

    def reset(self):
        logger.info("Reseting Server")
        self.stop()
        self.updaters.clear()
        self.running_task.cancel()
        self.start()


server = Server()


async def main():
    server.start()


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
