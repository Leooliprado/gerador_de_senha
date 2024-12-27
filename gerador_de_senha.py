import time
import requests
import hashlib
from PIL import Image
from io import BytesIO

# Função para processar os pixels da imagem e calcular a soma
def processar_imagem(img):
    pixels = img.load()
    soma = 0
    pixels_data = []

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]  # Pega o valor RGB do pixel
            # Soma os valores RGB para criar um "número" do pixel
            numero = r + g + b
            soma += numero
            pixels_data.append((x, y, numero))

    return pixels_data, soma


while True:
    time.sleep(1)
    # Baixar a imagem
    response = requests.get('https://picsum.photos/500')  # 500x500 image
    img = Image.open(BytesIO(response.content))

    # Processar a imagem e obter os dados dos pixels e a soma
    pixels_data, soma_imagem = processar_imagem(img)

    # Exibir soma dos valores dos pixels
    print(f'Soma dos Valores dos Pixels: {soma_imagem}')

    # Configurações da API e cidade
    api_key = ""
    city_name = ""

    # URL da API
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key + "&units=metric"

    # Fazendo a solicitação
    response = requests.get(complete_url)
    data = response.json()

    # Verificando se a solicitação foi bem-sucedida
    if data["cod"] == 200:
        # Coordenadas
        coord_lon = data["coord"]["lon"]
        coord_lat = data["coord"]["lat"]

        # Condições atmosféricas
        weather_main = data["weather"][0]["main"]
        weather_description = data["weather"][0]["description"]

        # Convertendo strings em valores numéricos via hashing
        weather_main_hash = int(hashlib.sha256(weather_main.encode()).hexdigest(), 16) % 100
        weather_description_hash = int(hashlib.sha256(weather_description.encode()).hexdigest(), 16) % 100

        # Informações principais
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]

        # Gerando número pseudo-aleatório com base nos dados climáticos
        chaotic_number = (coord_lat * coord_lon * weather_main_hash * weather_description_hash * temp *
                        feels_like / temp_min / temp_max / pressure / humidity) % 100  # Normalizando para 0-99
        
        # Incorporando a soma da imagem no número final, para mais "caos"
        chaotic_number_final = (chaotic_number + soma_imagem) % 100  # Normalizando para 0-99
        
        print(f"Número aleatório =-=-=-=-=-=->>> {chaotic_number_final}\n\n")
    else:
        print(f"Erro ao obter os dados da API. Código de erro: {data['cod']}")
