import json
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template


class CoordinatorAgent(Agent):

    class HandleAlertBehaviour(CyclicBehaviour):

        async def run(self):
            msg = await self.receive(timeout=10)

            if msg:
                print("\n📨 Coordinator received alert")

                # Ensure body exists before parsing
                if not msg.body:
                    print("⚠️ Empty message body received")
                    return

                try:
                    data = json.loads(msg.body)
                except json.JSONDecodeError:
                    print("⚠️ Invalid JSON received")
                    return

                print("🚨 Fire Alert Data:", data)

                if data.get("fire_detected"):

                    location = data.get("location")

                    print(f"🔥 Fire confirmed at {location}")
                    print("📢 Assigning rescue task...")

                    # Rescue agents list
                    rescue_agents = [
                        "rescue_01@xmpp.jp",
                        "rescue_02@xmpp.jp"
                    ]

                    task = {
                        "task": "rescue",
                        "location": location,
                        "priority": "high"
                    }

                    for agent in rescue_agents:

                        task_msg = Message(to=agent)
                        task_msg.set_metadata("performative", "request")
                        task_msg.body = json.dumps(task)

                        await self.send(task_msg)

                        print(f"✅ Task sent to {agent}")

            else:
                import asyncio
                await asyncio.sleep(1)

    async def setup(self):
        print("🚑 Coordinator Agent started")

        template = Template()
        template.set_metadata("performative", "inform")

        self.add_behaviour(self.HandleAlertBehaviour(), template)