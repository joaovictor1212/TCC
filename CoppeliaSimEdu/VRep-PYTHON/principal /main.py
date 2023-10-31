import os
import scara
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import  requests
import base64
import io
import binascii

# Inicia Simulação
scara.start()

scara.get_camera()

# Primeiros testes de identificação de padrões
# ======================= Ajustar o caminho que pega a imagem ========================
img_rgb = cv.imread("/home/adduser/ADS/TCC/CoppeliaSimEdu/images/camera.png")


# Fazendo uma solicitação GET para o URL


class ValidationImages:

    @staticmethod
    def get_images_in_database():
        respostas = requests.get('http://localhost:8000/api/registros')
        # Verificando se a solicitação foi bem-sucedida (código de status 200)
        if respostas.status_code == 200:
            # Obtendo os dados da resposta como um dicionário Python
            dados = respostas.json()

            for dado in dados:
                # with open('./teste.txt', 'w') as arquivo:
                #  # Escrevendo a string no arquivo
                #     arquivo.write(dado.get('arquivo'))
                arquivo_base64 = dado.get('arquivo')
                imagem_bytes = base64.b64decode(arquivo_base64)
                # # Converter bytes para uma matriz NumPy
                imagem_np = np.frombuffer(imagem_bytes, np.uint8)

                # # Decodificar a matriz para uma imagem usando OpenCV
            
                # Ou cv2.IMREAD_COLOR para uma imagem colorida
                # imagem = cv.cvtColor(imagem_np, cv.COLOR_GRAY2BGR)  
                
                # Verificar o imdecode ou o cvtColor
                imagem = cv.imdecode(imagem_np, cv.IMREAD_COLOR) 
                
                # Exibir a imagem em uma janela usando OpenCV
                cv.imshow('Imagem TESTE', imagem)

                # Esperar até que uma tecla seja pressionada e fechar a janela
                cv.waitKey(0)
                cv.destroyAllWindows()
            return imagem
        else:
            # Se a solicitação não for bem-sucedida, imprima o código de status
            print('Falha na solicitação. Código de status:', respostas.status_code, respostas.text)

    @staticmethod
    def get_image_to_verify():
        assert os.path.exists('/home/adduser/ADS/TCC/CoppeliaSimEdu/images/camera.png'), "Arquivo não encontrado, verifique o caminho."
        # Lê a imagem RGB
        img_rgb = cv.imread('/home/adduser/ADS/TCC/CoppeliaSimEdu/images/camera.png')
        return img_rgb

    # @staticmethod
    # def mapping_imagens_with_template():
        # assert img_rgb is not None, "file could not be read, check with os.path.exists()"
        # img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        # template = cv.imread('../patterns/quadrado-vermelho.png', cv.IMREAD_GRAYSCALE)
        # assert template is not None, "file could not be read, check with os.path.exists()"
        # w, h = template.shape[::-1]
        # res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        # threshold = 0.8
        # loc = np.where(res >= threshold)
        # for pt in zip(*loc[::-1]):
        #     cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        # cv.imwrite('res.png', img_rgb)

    @staticmethod
    def mapping_imagens_with_template():
        
        # Obtém a imagem carregada pelo Vrep
        img_rgb = ValidationImages.get_image_to_verify()
        assert img_rgb is not None, "Imagem não pode ser lida, verifique o arquivo."
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY) 
        # Obtém o padrão (template) do banco de dados
        template = ValidationImages.get_images_in_database()
        assert template is not None, "Padrão não pode ser lido, verifique o arquivo."
        template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
        # Obtém as dimensões do template
        w, h= template_gray.shape[::-1]
        
        # Faz o matchTemplate
        res = cv.matchTemplate(img_gray, template_gray, cv.TM_CCOEFF_NORMED)
        
        threshold = 0.8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        
        # Salva a imagem com os retângulos desenhados
        cv.imwrite('/home/adduser/ADS/TCC/CoppeliaSimEdu/images/res.png', img_rgb)



    
    

ValidationImages.mapping_imagens_with_template()

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
