import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from transitions import Machine


# ----------------------------
# Fire Rescue FSM
# ----------------------------

class FireRescueFSM(object):

    states = ['idle', 'deploying', 'extinguishing', 'rescuing', 'reporting']

    def __init__(self):
        self.machine = Machine(model=self, states=FireRescueFSM.states, initial='idle')

        self.machine.add_transition('fire_alert', 'idle', 'deploying')
        self.machine.add_transition('arrive_scene', 'deploying', 'extinguishing')
        self.machine.add_transition('fire_out', 'extinguishing', 'rescuing')
        self.machine.add_transition('rescue_done', 'rescuing', 'reporting')
        self.machine.add_transition('report_sent', 'reporting', 'idle')


# ----------------------------
# Fire Rescue Agent
# ----------------------------

class FireRescueAgent(Agent):

    class FireBehaviour(CyclicBehaviour):

        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                event = msg.body
                print(f"[EVENT RECEIVED]: {event}")

                if event == "FIRE_ALERT" and self.agent.fsm.state == "idle":

                    self.agent.fsm.fire_alert()
                    print("State:", self.agent.fsm.state)

                    self.agent.fsm.arrive_scene()
                    print("State:", self.agent.fsm.state)

                    self.agent.fsm.fire_out()
                    print("State:", self.agent.fsm.state)

                    self.agent.fsm.rescue_done()
                    print("State:", self.agent.fsm.state)

                    self.agent.fsm.report_sent()
                    print("State:", self.agent.fsm.state)

    async def setup(self):
        print("🔥 Fire Rescue Agent starting...")
        self.fsm = FireRescueFSM()
        self.add_behaviour(self.FireBehaviour())


# ----------------------------
# Fire Sensor Agent
# ----------------------------

class FireSensorAgent(Agent):

    class SendFireAlert(CyclicBehaviour):

        async def run(self):
            await asyncio.sleep(5)

            msg = Message(to="jan_30@xmpp.jp")
            msg.body = "FIRE_ALERT"

            await self.send(msg)
            print("🚨 [SENSOR]: Fire outbreak detected! Alert sent.")

            await asyncio.sleep(10)
            await self.agent.stop()

    async def setup(self):
        print("🔥 Fire Sensor Agent starting...")
        self.add_behaviour(self.SendFireAlert())


# ----------------------------
# Main Execution
# ----------------------------

async def main():
    rescue = FireRescueAgent("jan_30@xmpp.jp", "jan2004")
    sensor = FireSensorAgent("cyberkid54@xmpp.jp", "jan2004")

    await rescue.start()
    await sensor.start()

    await asyncio.sleep(20)

    await rescue.stop()


if __name__ == "__main__":
    asyncio.run(main())