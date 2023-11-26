import os
import scara
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import requests
import base64
import io
import binascii
import imutils

# Inicia Simulação
scara.start()

scara.get_camera()

# Primeiros testes de identificação de padrões
# ======================= Ajustar o caminho que pega a imagem ========================
img_rgb = cv.imread("/home/joao/ADS/TCC/CoppeliaSimEdu/images/vrep.jpg")


# Fazendo uma solicitação GET para o URL


class ValidationImages:

    @staticmethod
    def get_images_in_database():
        respostas = requests.get('http://localhost:8000/api/registros')
        # Verificando se a solicitação foi bem-sucedida (código de status 200)
        if respostas.status_code == 200:
            # Obtendo os dados da resposta como um dicionário Python
            dados = respostas.json()
            imagens_coordenadas = []
            count = 0
            for dado in dados:
                arquivo_base64 = dado.get('arquivo')
                x = dado.get('coordenada_x')
                y = dado.get('coordenada_y')
                imagem_bytes = base64.b64decode(arquivo_base64)
                # # Converter bytes para uma matriz NumPy
                imagem_np = np.frombuffer(imagem_bytes, np.uint8)
                # # Decodificar a matriz para uma imagem usando OpenCV

                # # Ou cv2.IMREAD_COLOR para uma imagem colorida
                # imagem = cv.cvtColor(imagem_np, cv.COLOR_GRAY2BGR)  

                # Verificar o imdecode ou o cvtColor
                imagem = cv.imdecode(imagem_np, cv.IMREAD_COLOR)

                # Exibir a imagem em uma janela usando OpenCV
                cv.imshow('Imagem TESTE', imagem)
                # Esperar até que uma tecla seja pressionada e fechar a janela
                cv.waitKey(0)
                cv.destroyAllWindows()

                dict_image = {
                    'nome': count,
                    'imagem': imagem,
                    'x': x,
                    'y': y,
                }
                count += 1
                imagens_coordenadas.append(dict_image)

            return imagens_coordenadas
        else:
            # Se a solicitação não for bem-sucedida, imprima o código de status
            print('Falha na solicitação. Código de status:', respostas.status_code, respostas.text)

    @staticmethod
    def mapping_imagens_with_template():
        import pdb;pdb.set_trace()
        global img_rgb
        assert img_rgb is not None, "file could not be read, check with os.path.exists()"
        alturaVrep, larguraVrep, channelsVrep = img_rgb.shape
        img_rgb = imutils.resize(img_rgb, width=round(larguraVrep * 0.5))

        # Pegando os padroes no banco
        padroes = None
        padroes = ValidationImages.get_images_in_database()

        if padroes:
            for padrao in padroes:
                nome = "IMAGEM-" + str(padrao.get('nome'))
                template = cv.cvtColor(padrao.get('imagem'), cv.COLOR_BGR2RGB)
                assert template is not None, "file could not be read, check with os.path.exists()"
                alturaTemplate, larguraTemplate, channelsTemplate = template.shape
                template = imutils.resize(template, width=round(larguraTemplate * 0.5))

                res = cv.matchTemplate(img_rgb, template, cv.TM_CCOEFF_NORMED, )

                minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(res)

                print(minVal, maxVal)
                if maxVal > 0.8:
                    ValidationImages.create_result_image(nome=nome, maxLoc=maxLoc, img_rgb=img_rgb,
                                                         largura=larguraTemplate, altura=alturaTemplate)
                    ValidationImages.move_in_vrep(coordenada_x=padrao.get('x'), coordenada_y=padrao.get('y'))
                else:
                    print("Padrão %s não conseguiu realizar o macthTemplate." % nome)
                    continue


    @staticmethod
    def create_result_image(maxLoc, img_rgb, altura, largura, nome):
        (startX, startY) = maxLoc
        endX = startX + largura
        endY = startY + altura

        # Desenhando retângulo de detecção
        color = (255, 0, 0)
        cv.rectangle(img_rgb, (startX, startY), (endX, endY), color, 3)
        cv.imwrite('/home/joao/ADS/TCC/CoppeliaSimEdu/images/result.png', img_rgb)
        print("Padrão %s conseguiu realizar o matchTemplate." % nome)



    @staticmethod
    def move_in_vrep(coordenada_x, coordenada_y):
        if coordenada_x and coordenada_y:
            x = float(coordenada_x)
            y = float(coordenada_y)
            scara.moveJ(x, y)
            scara.moveJ((x - x), (y - y))
            scara.moveJ((x - x), (0 - y))
            scara.moveJ((x - x), (y - y))
            scara.stop()




ValidationImages.mapping_imagens_with_template()


