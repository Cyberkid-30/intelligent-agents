from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade import run


class HelloAgent(Agent):
    class SayHelloBehaviour(OneShotBehaviour):
        async def run(self):
            print(f"Hello! I am agent {self.agent.jid}")
            await self.agent.stop()

    async def setup(self):
        print("Agent starting...")
        self.add_behaviour(self.SayHelloBehaviour())


async def main():
    agent = HelloAgent(
        "jan_30@xmpp.jp",
        "jan2004"
    )
    await agent.start()


if __name__ == "__main__":
    run(main())
