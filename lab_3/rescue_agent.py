from transitions import Machine

class RescueAgent:

    states = [
        'Idle',
        'Patrol',
        'RescueVictim',
        'RespondToFire',
        'AvoidObstacle',
        'Completed'
    ]

    def __init__(self):

        self.previous_state = None

        self.machine = Machine(
            model=self,
            states=RescueAgent.states,
            initial='Idle'
        )

        # Mission transitions
        self.machine.add_transition('start', 'Idle', 'Patrol')
        self.machine.add_transition('victim', 'Patrol', 'RescueVictim')
        self.machine.add_transition('fire', 'Patrol', 'RespondToFire')
        self.machine.add_transition('done',
                                    ['RescueVictim','RespondToFire'],
                                    'Completed')

        self.machine.add_transition(
            'obstacle',
            '*',
            'AvoidObstacle',
            before='save_state'
        )

        self.machine.add_transition(
            'clear',
            'AvoidObstacle',
            'Idle',           # temporary placeholder
            after='restore_state'
        )
    


    def restore_state(self):
        if self.previous_state:
            self.state = self.previous_state

    def save_state(self):
        self.previous_state = self.state


# ===== Run Simulation =====

agent = RescueAgent()

print("Initial:", agent.state)

agent.start()
print("After start:", agent.state)

agent.victim()
print("Victim detected:", agent.state)

agent.obstacle()
print("Obstacle:", agent.state)

agent.clear()
print("Cleared:", agent.state)

agent.done()
print("Finished:", agent.state)
