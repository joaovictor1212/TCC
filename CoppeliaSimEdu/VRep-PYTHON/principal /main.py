import os
import scara
import cv2 as cv
import numpy as np 
import matplotlib.pyplot as plt
import  requests
import base64
import io
import binascii

# Inicia Simulação
scara.start()

scara.get_camera()

# Primeiros testes de identificação de padrões
# ======================= Ajustar o caminho que pega a imagem ========================
img_rgb = cv.imread("/home/adduser/ADS/TCC/CoppeliaSimEdu/images/vrep.jpg")


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
            
                # Ou cv2.IMREAD_COLOR para uma imagem colorida
                # imagem = cv.cvtColor(imagem_np, cv.COLOR_GRAY2BGR)  
                
                # Verificar o imdecode ou o cvtColor
                imagem = cv.imdecode(imagem_np, cv.IMREAD_COLOR) 
                
                cv.imshow("IMAGEM BANCO", imagem)
                cv.waitKey(0)
                cv.destroyAllWindows()
                
                dict_image = {
                    'nome' : count,
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
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        # import pdb;pdb.set_trace()
        assert img_gray is not None, "Arquivo não pode ser lido, check o caminho da imagem obtida no Vrep" #validacao
        print("Dimensões imagem vrep",img_gray.shape) #printa o tamanho da imagem
        img_gray2 = img_gray.copy() #transforma a imagem para cinza
        
        
        data = ValidationImages.get_images_in_database() #pega os registros no banco de dados
        if data:
            for template_database in data:
                if template_database:
                    
                    template_rgb = template_database.get('imagem') #pega o arquivo de imagem 
                    assert template_rgb is not None, "Arquivo não pode ser lido" #validacao
                    print("tamanho imagem do padrão", template_rgb.shape) #printa o tamanho
                    template_gray = cv.cvtColor(template_rgb , cv.COLOR_BGR2GRAY) #transforma para cinza
                    
                
                altura, largura = template_gray.shape[::-1]
                    
                res = cv.matchTemplate(img_gray, template_gray, cv.TM_SQDIFF)
                    
                threshold = 0.8
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
                nome = template_database.get('nome')
                if min_val >= threshold:
                    ValidationImages.create_result_image(nome=nome, max_loc=max_loc, img_rgb=img_rgb, largura=largura, altura=altura)
                    ValidationImages.move_in_vrep(coordenada_x=template_database.get('x'), coordenada_y=template_database.get('y'))
                    
                else:
                    print("Padrão %s não conseguiu realizar o macthTemplate." %nome)
                    continue    
                    
    
    @staticmethod
    def move_in_vrep(coordenada_x, coordenada_y):
        # import pdb;pdb.set_trace()
        if coordenada_x and coordenada_y:
            x = float(coordenada_x)
            y = float(coordenada_y)
            scara.moveJ(x, y)
            scara.moveJ((x - x), (y - y)) 
            scara.moveJ((x - x), (0 - y)) 
            scara.moveJ((x - x), (y - y))
        scara.stop()
    
    
    @staticmethod
    def create_result_image(max_loc, img_rgb, altura, largura, nome):
        top_left = max_loc
        # # Calculate the center of the square.
        center = (top_left[0] + largura / 2, top_left[1] + altura / 2)
        # Move the square to the desired location.
        center = (center[0] + 100, center[1] + 100)
        # Update the top_left and bottom_right coordinates of the square.
        top_left = (int(center[0] - largura / 2), int(center[1] - altura / 2))
        bottom_right = (top_left[0] + largura, top_left[1] + altura)
        # bottom_right = (top_left[0] + 100, top_left[1] + 100)
        color = (255, 255, 0)
        # cv.rectangle(img,top_left, bottom_right, 255, 2)
        cv.rectangle(img_rgb, top_left, bottom_right, color, 2)
        cv.imwrite('/home/adduser/ADS/TCC/CoppeliaSimEdu/images/result.png', img_rgb)
        print("Padrão %s conseguiu realizar o matchTemplate." %nome)





ValidationImages.mapping_imagens_with_template()

