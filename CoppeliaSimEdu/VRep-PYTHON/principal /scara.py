import time
from decimal import Decimal
from math import degrees, radians
from coppeliasim_zmqremoteapi_client import *

import sys

# sys.path.append("/home/adduser/ADS/TCC/CoppeliaSimEdu/programming/zmqRemoteApi/clients/python")

# from zmqRemoteApi import RemoteAPIClient

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
camera = sim.getObject("/Vision_sensor")

# max_speed = 6.28
# sim.setJointTargetVelocity(axis_A, 0, [max_speed, max_speed])
# sim.setJointTargetVelocity(axis_B, 0, [max_speed, max_speed])

# print(sim.getObjectFloatParam(axis_A, sim.jointfloatparam_maxvel))
# print(sim.getObjectFloatParam(axis_A, sim.jointfloatparam_maxjerk))

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

def moveJ(t1, t2, interpolation=True):
    """
    Movimenta para uma posição no espaço das juntas

    Parâmetros:
      t1, t2 = Ângulo das juntas (em graus)
      interoplation = Deve ser realizada a interpolação de tempo ou não (True | False), padrão True
    """

    # Configurações
    threshold = 0.01

    # Interpolation
    vel_max = 2
    vel_max_a = vel_max
    vel_max_b = vel_max

    if interpolation:
        s1, s2 = get_sensors()

        dif_elo_a = abs_dif(s1, t1)
        dif_elo_b = abs_dif(s2, t2)

        if dif_elo_a < dif_elo_b and dif_elo_a >= threshold:
            delta_t_a = dif_elo_a / vel_max_a
            vel_max_b = dif_elo_b / delta_t_a
        if dif_elo_b > dif_elo_a and dif_elo_b >= threshold:
            delta_t_b = dif_elo_b / vel_max_b
            vel_max_a = dif_elo_a / delta_t_b

    sim.setJointTargetVelocity(axis_A, 0, [vel_max_a, vel_max_a])
    sim.setJointTargetVelocity(axis_B, 0, [vel_max_b, vel_max_b])

    # End Interpolation

    sim.setJointTargetPosition(axis_A, radians(t1))
    sim.setJointTargetPosition(axis_B, radians(t2))

    while True:
        s1, s2 = get_sensors()

        moved_a = True if abs(s1 - t1) <= threshold else False
        moved_b = True if abs(s2 - t2) <= threshold else False

        if moved_a and moved_b:
            break

        client.step()


def get_camera():
    img, res = sim.getVisionSensorImg(camera)
    sim.saveImage(img, res, 0, "images/camera.png", -1)
