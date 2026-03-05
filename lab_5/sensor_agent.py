import json
import random
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class SensorAgent(Agent):

    class DetectFireBehaviour(OneShotBehaviour):

        async def run(self):

            temperature = 60 # random.randint(20, 100)
            smoke = 80 # random.randint(0, 100)

            print(f"\n🌡 Temperature: {temperature}")
            print(f"💨 Smoke Level: {smoke}")

            fire_detected = temperature > 50 and smoke > 70

            if fire_detected:

                print("🔥 FIRE DETECTED")

                msg = Message(to="coordinator_01@xmpp.jp")
                msg.set_metadata("performative", "inform")

                msg.body = json.dumps({
                    "fire_detected": True,
                    "temperature": temperature,
                    "smoke_level": smoke,
                    "location": "Building-A Floor 3"
                })

                await self.send(msg)

                print("📤 Sensor sent alert to Coordinator")

            else:
                print("✅ Environment safe")

    async def setup(self):
        print("Sensor Agent started")
        self.add_behaviour(self.DetectFireBehaviour())