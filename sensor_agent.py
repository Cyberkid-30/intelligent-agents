import asyncio
from spade import run
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from datetime import datetime
import random

class DisasterEnvironment:
    """
    Simulates a disaster environment with random events.
    """
    def __init__(self):
        self.events = ["Fire", "Flood", "Earthquake", "Gas Leak"]

    def generate_event(self):
        """
        Randomly generate a disaster event with a severity level.
        """
        event = random.choice(self.events)
        severity = random.randint(1, 10)  # 1 = low, 10 = high
        return {"event": event, "severity": severity}

class SensorAgent(Agent):
    class SenseEnvironmentBehaviour(CyclicBehaviour):
        async def run(self):
            event = self.agent.environment.generate_event()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] {self.agent.jid} sensed: {event['event']} (Severity: {event['severity']})"
            
            # Print to terminal
            print(log_message)
            
            # Append to log file
            with open("sensor_events.log", "a") as f:
                f.write(log_message + "\n")
            
            # Wait before next sensing
            await asyncio.sleep(2)  # senses every 2 seconds

    async def setup(self):
        print(f"{self.jid} starting SensorAgent...")
        self.add_behaviour(self.SenseEnvironmentBehaviour())

async def main():
    # Create environment
    environment = DisasterEnvironment()

    # Create SensorAgent
    sensor_agent = SensorAgent("sensor@localhost", "sensor123")
    sensor_agent.environment = environment

    # Start agent with auto registration
    await sensor_agent.start(auto_register=True)

    # Keep it running for a while (simulate ongoing perception)
    await asyncio.sleep(15)
    await sensor_agent.stop()

if __name__ == "__main__":
    run(main())
