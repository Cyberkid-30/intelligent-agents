import random
import json
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class SensorAgent(Agent):

    class FireDetectionBehaviour(OneShotBehaviour):
        async def run(self):

            # Simulated environmental readings
            temperature = random.randint(20, 100)
            smoke_level = random.randint(0, 100)
            location = "Building-A, Floor 3"

            print(f"🌡 Temperature: {temperature}°C")
            print(f"💨 Smoke Level: {smoke_level}%")

            # Fire detection rule
            fire_detected = temperature > 50 and smoke_level > 70

            if fire_detected:
                print("🔥 FIRE DETECTED!")

                # Sensor Agent — sending INFORM (JSON structured)
                msg = Message(to="coordinator_01@xmpp.jp")
                msg.set_metadata("performative", "inform")
                msg.set_metadata("ontology", "disaster-management")

                msg.body = json.dumps({
                    "fire_detected": True,
                    "temperature": temperature,
                    "smoke_level": smoke_level,
                    "location": location
                })

                await self.send(msg)
                print("📤 INFORM message sent to Coordinator.")

            else:
                print("✅ Environment safe. No fire detected.")

    async def setup(self):
        print("✅ Sensor Agent started")
        self.add_behaviour(self.FireDetectionBehaviour())