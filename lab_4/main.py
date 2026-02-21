import asyncio
import logging
from loguru import logger
from sensor_agent import SensorAgent
from coordinator_agent import CoordinatorAgent
from rescue_agent import RescueAgent

# Suppress SPADE/XMPP internal logs
logger.disable("spade")
logger.disable("aioxmpp")
logger.disable("aiosasl")
logging.disable(logging.CRITICAL)


async def main():

    # Replace passwords with your actual XMPP credentials
    sensor = SensorAgent("sensor_01@xmpp.jp", "123456")
    coordinator = CoordinatorAgent("coordinator_01@xmpp.jp", "123456")
    rescue = RescueAgent("rescue_01@xmpp.jp", "123456")

    await rescue.start()
    await coordinator.start()
    await sensor.start()

    print("\n🚀 All agents started...\n")

    # Keep system running long enough for one full message exchange
    await asyncio.sleep(10)

    await sensor.stop()
    await coordinator.stop()
    await rescue.stop()

    print("\n🛑 All agents stopped.")


if __name__ == "__main__":
    asyncio.run(main())