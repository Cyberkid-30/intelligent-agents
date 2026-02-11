import asyncio
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message


# =========================
# SENSOR AGENT
# =========================

class SensorAgent(Agent):

    class RespondStatus(CyclicBehaviour):

        async def run(self):
            msg = await self.receive(timeout=10)

            if msg:
                perf = msg.get_metadata("performative")

                # Parse REQUEST
                if perf == "request":
                    print("\n[Sensor] REQUEST received")

                    # Simulate sensing
                    victims = random.randint(0, 3)

                    info = Message(to=str(msg.sender))
                    info.set_metadata("performative", "inform")
                    info.body = f"Victims detected: {victims}"

                    await self.send(info)

                    print("[Sensor] INFORM sent:", info.body)

    async def setup(self):
        print("Sensor Agent running")
        self.add_behaviour(self.RespondStatus())


# =========================
# COORDINATOR AGENT
# =========================

class CoordinatorAgent(Agent):

    class RequestStatus(OneShotBehaviour):

        async def run(self):
            print("\n[Coordinator] Requesting sensor report")

            req = Message(to="jan_30@xmpp.jp")
            req.set_metadata("performative", "request")
            req.body = "Send victim report"

            await self.send(req)

            reply = await self.receive(timeout=10)

            if reply:
                print("[Coordinator] INFORM received:", reply.body)

                # Parse message content
                number = int(reply.body.split(":")[1])

                # Trigger action
                if number > 0:
                    print("[Coordinator] Action: Dispatch rescue team")
                else:
                    print("[Coordinator] Action: Continue patrol")

            await self.agent.stop()

    async def setup(self):
        print("Coordinator Agent running")
        self.add_behaviour(self.RequestStatus())


# =========================
# MAIN EXECUTION
# =========================

async def main():

    sensor = SensorAgent("jan_30@xmpp.jp", "jan2004")
    coordinator = CoordinatorAgent("cyberkid54@xmpp.jp", "jan2004")

    await sensor.start()
    await coordinator.start()

    await asyncio.sleep(10)

    await sensor.stop()


if __name__ == "__main__":
    asyncio.run(main())
