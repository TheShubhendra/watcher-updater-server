import logging
import asyncio
from watcher import Watcher
import updater.database_api as api
from decouple import config
from watcher.events.quora import QuoraEvent
import json
import aiohttp


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=logging.DEBUG,
)

UPDATER_ID = config("UPDATER_ID")
logger = logging.getLogger(__name__)
CALLBACK_SERVER = config("CALLBACK_SERVER")


def event_handler(event):
    logger.info("Sending an event")
    async with aiohttp.ClientSession() as session:
        await session.post(CALLBACK_SERVER, json=json.dumps(event))

class Server(Watcher):
    def start(self):
        logger.info("Starting Server")
        users = api.fetch_usernames(UPDATER_ID)
        for id, usernames in users:
            self.add_quora(usernames, update_interval=3)
        self.dispatcher.add_handler(QuoraEvent, event_handler)
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



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        asyncio.gather(task)
        task.cancel()
        logger.info("Closing loop")
        pass
    loop.close()
