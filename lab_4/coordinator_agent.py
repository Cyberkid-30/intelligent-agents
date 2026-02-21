from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class CoordinatorAgent(Agent):

    class ReceiveAlertBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"📥 [Coordinator] Received: {msg.body}")

                if msg.get_metadata("performative") == "inform":
                    print("🧠 [Coordinator] Processing alert...")

                    request = Message(
                        to="rescue_01@xmpp.jp",
                        body="Fire outbreak at Sector A. Immediate response required."
                    )

                    request.set_metadata("performative", "request")
                    request.set_metadata("ontology", "disaster-management")

                    await self.send(request)
                    print("📤 [Coordinator] REQUEST sent to Rescue.")

                    self.kill()  # Stop after handling one alert

    async def setup(self):
        print("✅ Coordinator Agent started")
        self.add_behaviour(self.ReceiveAlertBehaviour())