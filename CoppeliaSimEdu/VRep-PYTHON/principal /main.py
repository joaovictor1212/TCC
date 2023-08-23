import scara
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


# Inicia Simulação
scara.start()

scara.get_camera()

# Primeiros testes de identificação de padrões
img_rgb = cv.imread("/home/adduser/ADS/TCC/CoppeliaSimEdu/images/camera.png")

assert img_rgb is not None, "file could not be read, check with os.path.exists()"
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread('../patterns/quadrado-vermelho.png', cv.IMREAD_GRAYSCALE)
assert template is not None, "file could not be read, check with os.path.exists()"
w, h = template.shape[::-1]
res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
cv.imwrite('res.png', img_rgb)

# scara.moveJ(0, 90)
# scara.moveJ(0, 0)
# scara.moveJ(0, -90)
# scara.moveJ(0, 0)

# scara.moveJ(90, 0)
# scara.moveJ(0, 0)
# scara.moveJ(-90, 0)
# scara.moveJ(0, 0)


# Finaliza Simulação
scara.stop()
