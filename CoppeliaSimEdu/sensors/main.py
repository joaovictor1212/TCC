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
img_rgb = cv.imread("/home/adduser/ADS/TCC/CoppeliaSimEdu/images/vrep.png")


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
                x = dado.get('coordenada_x')
                y = dado.get('coordenada_y')
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
                # template_gray = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
                
            return imagem, x, y
        else:
            # Se a solicitação não for bem-sucedida, imprima o código de status
            print('Falha na solicitação. Código de status:', respostas.status_code, respostas.text)

    # @staticmethod
    # def get_image_to_verify():
    #     assert os.path.exists('/home/adduser/ADS/TCC/CoppeliaSimEdu/images/camera.png'), "Arquivo não encontrado, verifique o caminho."
    #     # Lê a imagem RGB
    #     img_rgb = cv.imread('/home/adduser/ADS/TCC/CoppeliaSimEdu/images/camera.png')
    #     # img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    #     return img_rgb

    
    # @staticmethod
    # def mapping_imagens_with_template():
    #     import pdb;pdb.set_trace()
    #     # Obtém a imagem carregada pelo Vrep
    #     assert img_rgb is not None, "VERIFIQUE a IMAGEM"
    #     img_r, img_g, img_b = cv.split(img_rgb)
    #     assert img_r is not None, "Imagem não pode ser lida, verifique o arquivo."
    #     assert img_g is not None, "Imagem não pode ser lida, verifique o arquivo."
    #     assert img_b is not None, "Imagem não pode ser lida, verifique o arquivo."
    #     # Obtém o padrão (template) do banco de dados
    #     template = ValidationImages.get_images_in_database()
    #     template_r, template_g, template_b = cv.split(template)
    #     assert template_r is not None, "Padrão não pode ser lido, verifique o arquivo."
    #     assert template_g is not None, "Padrão não pode ser lido, verifique o arquivo."
    #     assert template_b is not None, "Padrão não pode ser lido, verifique o arquivo."
    #     # Realizar a correspondência nos canais de cores individuais
    #     res_b = cv.matchTemplate(img_b, template_b, cv.TM_CCOEFF_NORMED)
    #     res_g = cv.matchTemplate(img_g, template_g, cv.TM_CCOEFF_NORMED)
    #     res_r = cv.matchTemplate(img_r, template_r, cv.TM_CCOEFF_NORMED)
    #     # Combinar os resultados dos canais de cores
    #     res = res_b + res_g + res_r
    #     # Definir um limite para os resultados
    #     threshold = 0.8
    #     # Encontrar as correspondências acima do limite
    #     loc = np.where(res >= threshold)
    #     # Desenhar retângulos nas correspondências encontradas na imagem original
    #     for pt in zip(*loc[::-1]):
    #         color = (65, 255, 98)  # Cor verde para os retângulos
    #         bottom_right = (pt[0] + template.shape[1], pt[1] + template.shape[0])
    #         cv.rectangle(img_rgb, pt, bottom_right, color, 2)
    #     # Salvar a imagem com os retângulos desenhados
    #     cv.imwrite('/home/adduser/ADS/TCC/CoppeliaSimEdu/images/result.png', img_rgb)
        


    # @staticmethod
    # def mapping_imagens_with_template():
    #     assert img_rgb is not None, "VERIFIQUE A IMAGEM"
    #     template = ValidationImages.get_images_in_database()
    #     img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    #     template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
    #     cv.normalize(img_gray, img_gray, 0, 255, cv.NORM_MINMAX)
    #     cv.normalize(template_gray, template_gray, 0, 255, cv.NORM_MINMAX)

    #     # Obtém as dimensões do template
    #     w = img_rgb.shape[1] - template.shape[1] + 1
    #     h = img_rgb.shape[0] - template.shape[0] + 1
    #     # Faz o matchTemplate
    #     res = cv.matchTemplate(img_gray, template_gray, cv.TM_CCOEFF_NORMED)
    #     (minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(res)
    #     (startX, startY) = maxLoc
    #     endX = startX + template.shape[1]
    #     endY = startY + template.shape[0]
        
    #     threshold = 0.7
    #     loc = np.where(res >= threshold)
    #     for pt in zip(*loc[::-1]):
    #         color = (65, 255, 85)  # Green color for rectangles
    #         cv2.rectangle(img_rgb, (startX, startY), (endX, endY), color, 3)
        
    #     # Salva a imagem com os retângulos desenhados
    #     cv.imwrite('/home/adduser/ADS/TCC/CoppeliaSimEdu/images/res.png', img_rgb)



    @staticmethod
    def mapping_imagens_with_template():
        import pdb;pdb.set_trace()
        assert img_rgb is not None, "file could not be read, check with os.path.exists()"
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        template_database, x, y = ValidationImages.get_images_in_database()
        template = cv.cvtColor(template_database, cv.COLOR_BGR2GRAY)
        assert template is not None, "file could not be read, check with os.path.exists()"
        h, w = template.shape
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            color = (16,78,100)
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), color, 2)
        cv.imwrite('/home/adduser/ADS/TCC/CoppeliaSimEdu/images/result.png', img_rgb)
        
        if x and y:
            int(x) 
            int(y)
            scara.moveJ(x, y) 
            scara.moveJ((x - x), (y - y)) 
            scara.moveJ((x - x), (0 - y)) 
            scara.moveJ((x - x), (y - y)) 



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
