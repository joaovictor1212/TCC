import scara
import time

# Inicia Simulação
scara.start()

scara.moveJ(0, 90)
scara.moveJ(0, 0)
scara.moveJ(0, -90)
scara.moveJ(0, 0)

scara.moveJ(90, 0)
scara.moveJ(0, 0)
scara.moveJ(-90, 0)
scara.moveJ(0, 0)


# Finaliza Simulação
scara.stop()
