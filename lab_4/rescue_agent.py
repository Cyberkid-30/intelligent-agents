from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class RescueAgent(Agent):

    class RescueBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"🚑 [Rescue] Received: {msg.body}")

                if msg.get_metadata("performative") == "request":
                    print("🚒 [Rescue] Dispatching team...")

                    reply = Message(
                        to=str(msg.sender),
                        body="Rescue team dispatched to Sector A."
                    )

                    reply.set_metadata("performative", "inform")
                    reply.set_metadata("ontology", "disaster-management")

                    await self.send(reply)
                    print("📤 [Rescue] INFORM confirmation sent.")

                    self.kill()  # Stop after handling one request

    async def setup(self):
        print("✅ Rescue Agent started")
        self.add_behaviour(self.RescueBehaviour())