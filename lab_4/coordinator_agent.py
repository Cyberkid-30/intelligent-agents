import json
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class CoordinatorAgent(Agent):

    class ReceiveAlertBehaviour(CyclicBehaviour):
        async def run(self):

            msg = await self.receive(timeout=10)

            if msg:
                print("📥 [Coordinator] Message received.")

                if msg.get_metadata("performative") == "inform":

                    # Parse JSON data from Sensor
                    data = json.loads(msg.body)

                    fire_detected = data.get("fire_detected", False)
                    temperature = data.get("temperature")
                    smoke_level = data.get("smoke_level")
                    location = data.get("location")

                    if fire_detected:
                        print("🔥 [Coordinator] Fire confirmed!")
                        print(f"   Location: {location}")
                        print(f"   Temp: {temperature}°C")
                        print(f"   Smoke: {smoke_level}%")

                        # Send structured REQUEST to Rescue Agent
                        request = Message(to="rescue_01@xmpp.jp")
                        request.set_metadata("performative", "request")
                        request.set_metadata("ontology", "disaster-management")

                        request.body = json.dumps({
                            "action": "dispatch_rescue_team",
                            "location": location,
                            "temperature": temperature,
                            "smoke_level": smoke_level,
                            "priority": "high"
                        })

                        await self.send(request)
                        print("📤 [Coordinator] REQUEST sent to Rescue.")

            else:
                print("[Coordinator] Waiting for alerts...")

    async def setup(self):
        print("✅ Coordinator Agent started")
        self.add_behaviour(self.ReceiveAlertBehaviour())