import argparse
import cv2
import imutils

# Imagem que o VREP tirou
image = cv2.imread("./vrep.png")

# Lista de padrões que existem no banco
lista_padroes = ["TESTE_QA.png"]

for pattern in lista_padroes:
    # Carregando imagem de
    template = cv2.imread(pattern)

    # Redimensionando imagens para 50% do tamanho
    height, width, channels = image.shape 
    image = imutils.resize(image, width=round(width * 0.5))
    import pdb;pdb.set_trace()
    height, width, channels = template.shape 
    template = imutils.resize(template, width=round(width * 0.5))

    # Exibindo imagens carregadas
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    
    cv2.imshow("Template", template)
    cv2.waitKey(0)

    # Convertendo para tons de cinza
    # Vamos pular essa etapa por enquanto

    # imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Executando reconhecimento de padrão
    # Caso deseje voltar para as imagens em tons de cinza, é necessário alterar a linha a seguir
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED, )

    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

    # Vamos tentar evitar falsos positivos
    # Vamos buscar por uma acurávia de -80% e + 80%

    if minVal < -0.6 or maxVal > 0.6:
        print(minVal, maxVal)

        # Determinando o retângulo de detecção
        (startX, startY) = maxLoc
        endX = startX + template.shape[1]
        endY = startY + template.shape[0]

        # Desenhando retângulo de detecção
        cv2.rectangle(image, (startX, startY), (endX, endY), (255, 0, 0), 3)

        # Exibindo resultado
        cv2.imshow("Output", image)
        cv2.waitKey(0)
    else:
        print("O padrão não foi encontrado na imagem")
