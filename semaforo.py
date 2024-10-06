from random import choice
from experta import *


class Light(Fact):
    """Info about the traffic light."""
    pass


class RobotCrossStreet(KnowledgeEngine):
    @Rule(Light(color='green'))
    def green_light(self):
        print("el semaforo esta en verde, puedes cruzar")

    @Rule(Light(color='red'))
    def red_light(self):
        print("el semaforo esta en rojo, no puedes cruzar")

    @Rule(AS.light << Light(color=L('yellow') | L('blinking-yellow')))
    def cautious(self, light):
        print("precaucion no puedes pasar ", light["color"])

#// Instantiate the engine and run it
engine = RobotCrossStreet()
#// Reset the engine and declare a new fact
engine.reset()

ciclo = 'S'
while ciclo == 'S' or ciclo == 's':
    print("Sistema experto decide si puedes cruzar la calle")
    color = input("Ingrese el color del semaforo: (V): verde, (R): rojo, (A): amarillo, (A1): amarillo intermitente: ")
    if color == 'V' or color == 'v':
        engine.declare(Light(color=choice(['green'])))
        engine.run()

    elif color == 'R' or color == 'r':
        engine.declare(Light(color=choice(['red'])))
    elif color == 'A' or color == 'a':
        engine.declare(Light(color=choice(['yellow'])))
    elif color == 'A1' or color == 'a1':
        engine.declare(Light(color=choice(['blinking-yellow'])))
    else:
        print("Opcion no valida")
    ciclo = input("Desea continuar? (S/N): ")
#// Run the engine
    engine.run()
#// Reset the engine

#// Declare a new fact
engine.declare(Light(color=choice(['green'])))


