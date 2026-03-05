import asyncio
from sensor_agent import SensorAgent
from coordinator_agent import CoordinatorAgent
from rescue_agent import RescueAgent


async def main():

    sensor = SensorAgent("sensor_01@xmpp.jp", "123456")
    coordinator = CoordinatorAgent("coordinator_01@xmpp.jp", "123456")

    rescue1 = RescueAgent("rescue_01@xmpp.jp", "123456")
    rescue2 = RescueAgent("rescue_02@xmpp.jp", "123456")

    await sensor.start()
    await coordinator.start()
    await rescue1.start()
    await rescue2.start()

    print("\n🚀 All agents started\n")

    await asyncio.sleep(20)

    await sensor.stop()
    await coordinator.stop()
    await rescue1.stop()
    await rescue2.stop()

    print("\n🛑 System shutdown")


if __name__ == "__main__":
    asyncio.run(main())