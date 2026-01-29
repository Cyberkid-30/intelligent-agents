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
        "agent1@localhost",
        "agent123"
    )
    await agent.start()





async def simulate_agent(name="Agent1", cycles=10):
    import asyncio
    import sys
    """
    Simulates an agent running in the terminal with a live activity animation.
    """
    print(f"{name} starting...")
    for i in range(cycles):
        # Simulate some “thinking” or “processing”
        for symbol in "|/-\\":
            sys.stdout.write(f"\r{name} running... {symbol}")
            sys.stdout.flush()
            await asyncio.sleep(0.2)
    print(f"\n{name} has completed its tasks.")

# Example usage
if __name__ == "__main__":
    import asyncio
    asyncio.run(simulate_agent("Agent1", cycles=15))




if __name__ == "__main__":
    run(main())
