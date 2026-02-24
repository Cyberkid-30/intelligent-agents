import json
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class RescueAgent(Agent):

    class RescueBehaviour(CyclicBehaviour):
        async def run(self):

            msg = await self.receive(timeout=10)

            if msg:
                print("🚑 [Rescue] Message received.")

                if msg.get_metadata("performative") == "request":

                    # Parse structured JSON request
                    data = json.loads(msg.body)

                    action = data.get("action")
                    location = data.get("location")
                    temperature = data.get("temperature")
                    smoke_level = data.get("smoke_level")
                    priority = data.get("priority")

                    print("🔥 [Rescue] Emergency Details:")
                    print(f"   Action: {action}")
                    print(f"   Location: {location}")
                    print(f"   Temp: {temperature}°C")
                    print(f"   Smoke: {smoke_level}%")
                    print(f"   Priority: {priority}")

                    # Simulate dispatch decision
                    print("🚒 [Rescue] Dispatching rescue team...")

                    # Send structured INFORM confirmation
                    reply = Message(to=str(msg.sender))
                    reply.set_metadata("performative", "inform")
                    reply.set_metadata("ontology", "disaster-management")

                    reply.body = json.dumps({
                        "status": "team_dispatched",
                        "location": location,
                        "response_unit": "Unit-Alpha",
                        "estimated_arrival": "5 minutes"
                    })

                    await self.send(reply)
                    print("📤 [Rescue] INFORM confirmation sent.")

            else:
                print("[Rescue] Waiting for emergency requests...")

    async def setup(self):
        print("✅ Rescue Agent started")
        self.add_behaviour(self.RescueBehaviour())