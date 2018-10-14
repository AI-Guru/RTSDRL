import time
from rtsdrl import Environment, Entity, Harvester, Resource, PyGameRenderer


# Create the environment and add some entities.
environment = Environment()
environment.add_entity(Harvester(50.0, 50.0, "harvester1"))
environment.add_entity(Harvester(150.0, 50.0, "harvester2"))
environment.add_entity(Harvester(100.0, -100.0, "harvester3"))
environment.add_entity(Resource(100.0, 100.0, "resource1"))

# Create the renderer.
renderer = PyGameRenderer()

# Run for a couple of steps.
for _ in range(100):
    renderer.render(environment)
    percepts = environment.get_percepts()
    environment.update(actions=[("harvester1", "turn_left"), ("harvester2", "turn_right"), ("harvester3", "move_forward")])
    #time.sleep(0.1)

#http://adventuresinmachinelearning.com/reinforcement-learning-tutorial-python-keras/

# TODO handle collisions
# TODO optimize speed


renderer.finish()
