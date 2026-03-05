import json
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class RescueAgent(Agent):

    class HandleTaskBehaviour(CyclicBehaviour):

        async def run(self):

            msg = await self.receive(timeout=10)

            if msg:

                # Ignore messages without body
                if not msg.body:
                    return

                # Only process REQUEST messages
                if msg.get_metadata("performative") != "request":
                    return

                data = json.loads(msg.body)

                location = data["location"]

                print(f"\n🚑 {self.agent.name} received rescue task for {location}")

                decision = random.choice(["accept", "refuse"])

                reply = Message(to=str(msg.sender))

                if decision == "accept":

                    reply.set_metadata("performative", "accept")
                    reply.body = json.dumps({"status": "accepted"})

                    print(f"✅ {self.agent.name} ACCEPTED task")

                else:

                    reply.set_metadata("performative", "refuse")
                    reply.body = json.dumps({"status": "rejected"})

                    print(f"❌ {self.agent.name} REFUSED task")

                await self.send(reply)

    async def setup(self):
        print(f"{self.name} started")
        self.add_behaviour(self.HandleTaskBehaviour())