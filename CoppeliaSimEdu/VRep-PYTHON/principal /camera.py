from coppeliasim_zmqremoteapi_client import *

from zmqRemoteApi import RemoteAPIClient

sys.path.append("/home/adduser/ADS/TCC/CoppeliaSimEdu/programming/zmqRemoteApi/clients/python")

camera = sim.getObject("/Vision_sensor")



def get_camera():
    img, res = sim.getVisionSensorImg(camera)
    sim.saveImage(img, res, 0, "images/camera.png", -1)
