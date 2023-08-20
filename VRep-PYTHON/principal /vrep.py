from zmqRemoteApi import RemoteAPIClient

client = RemoteAPIClient()
sim = client.getObject('sim')


def start():
    sim.startSimulation()


def stop():
    sim.stopSimulation()
