from math import cos, sin, atan2, degrees, radians, pow, acos
from decimal import *
import struct
import sys

sys.path.append(
    "/home/joaovictor/ADS/TCC/CoppeliaSimEdu/programming/zmqRemoteApi/clients/python")

from zmqRemoteApi import RemoteAPIClient

# Configurações Globais de Operação do Robô
tamanho_elo_1 = 0.4670
tamanho_elo_2 = 0.4005
precisao = 3

# Configura cliente de conexão com o CoppeliaSim
client = RemoteAPIClient()
sim = client.getObject('sim')
client.setStepping(False)

# Adquire handlers para as Juntas do Robô
axis_A = sim.getObject("/MTB/axis")
axis_B = sim.getObject("/MTB/axis/link/axis")
tool = sim.getObject("/MTB/axis/link/axis/link/axis/axis/link/link3Respondable/suctionPad/BodyRespondable")


abs_dif = lambda x, y: max(x, y) - min(x, y)



def start():
    """
    Inicia simulação no CoppeliaSim
    """
    print("Iniciando simulação")
    sim.startSimulation()

def stop():
    """
    Finaliza simulação no CoppeliaSim
    """
    input("Pressione a tecla Enter para finalizar a simulação ...")
    sim.stopSimulation()

def get_sensors():
    """
    Adquire posições de juntas do robô

    Retorno:
        t1, t2 = Posições das juntas dos Elos 1 e 2 (em graus)
    """
    t1 = sim.getJointPosition(axis_A)
    t2 = sim.getJointPosition(axis_B)

    t1 = round(degrees(t1), 3)
    t2 = round(degrees(t2), 3)

    return t1, t2
