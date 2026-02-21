from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
import random


class SensorAgent(Agent):

    class FireDetectionBehaviour(OneShotBehaviour):
        
        def check_environment(self):
            """Read temperature and smoke level from environment"""
            # Simulate sensor readings
            temperature = 73 # random.uniform(20, 80)  # in Celsius
            smoke_level = 64 # random.uniform(0, 100)  # in percentage/ppm
            
            return temperature, smoke_level
        
        def is_fire_detected(self, temperature, smoke_level):
            """Determine if fire exists based on temperature and smoke thresholds"""
            temp_threshold = 60  # Celsius
            smoke_threshold = 50  # ppm/percentage
            
            # Fire is detected if BOTH temperature is high AND smoke level is high
            fire_detected = temperature > temp_threshold and smoke_level > smoke_threshold
            
            return fire_detected
        
        async def run(self):
            # Check environment conditions
            temperature, smoke_level = self.check_environment()
            
            print(f"📊 [Sensor] Temperature: {temperature:.2f}°C")
            print(f"📊 [Sensor] Smoke Level: {smoke_level:.2f}%")
            
            # Analyze conditions for fire
            if self.is_fire_detected(temperature, smoke_level):
                print("🔥 [Sensor] FIRE DETECTED!")

                msg = Message(
                    to="coordinator_01@xmpp.jp",
                    body=f"Fire detected at Sector A! Temperature: {temperature:.2f}°C, Smoke: {smoke_level:.2f}%"
                )

                msg.set_metadata("performative", "inform")
                msg.set_metadata("ontology", "disaster-management")

                await self.send(msg)
                print("📤 [Sensor] INFORM sent to Coordinator.")
            else:
                print("✅ [Sensor] No fire detected - conditions normal.")

    async def setup(self):
        print("✅ Sensor Agent started")
        self.add_behaviour(self.FireDetectionBehaviour())