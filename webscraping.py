import requests
from bs4 import BeautifulSoup
# Ensure the 'schedule' library is installed by running 'pip install schedule' in the terminal.
import schedule
import time

#URL do site de notícias
url = "https://g1.globo.com/educacao/" \

## Fazendo a requisição para o site
response = requests.get(url)

#verifica se a requisição foi bem sucedida
if response.status_code == 200:
    # Cria o objeto BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontra todas as notícias na página
    noticias = soup.find_all('div', class_='widget--info__content')

    # Itera sobre as notícias e imprime o título e o link
    for noticia in noticias:
        titulo = noticia.find('a').text.strip()
        link = noticia.find('a')['href']
        print(f'Título: {titulo}')
        print(f'Link: {link}')
        print('-' * 80)
else:
    print(f'Erro ao acessar o site: {response.status_code}')

# Encontrando os títulos das notícias
noticias = soup.find_all('h3', class_='widget--info__title')

# Exibe os primeiros 10 títulos encontrados
for noticia in noticias[:10]:
    print(noticia.text.strip())

import pandas as pd

# Cria um DataFrame com os dados coletados
data = {
    'Título': [noticia.find('a').text.strip() for noticia in noticias],
    'Link': [noticia.find('a')['href'] for noticia in noticias]
}

df = pd.DataFrame(data)

# Salva o DataFrame em um arquivo CSV
df.to_csv('noticias_educacao.csv', index=False, encoding='utf-8-sig')

def coletar_noticias():
    # Faz a requisição novamente para coletar as notícias atualizadas
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        noticias = soup.find_all('div', class_='widget--info__content')
       
    if not noticias:
        print("Nenhuma notícia encontrada.")
        return
    else:
        print(f'Erro ao acessar o site: {response.status_code}')
        return

    dados = {
        'Título': [noticia.find('a').text.strip() for noticia in noticias]
    }
    df = pd.DataFrame(dados)

    nome_arquivo = 'noticias_educacao.csv'
    df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')
    print(f'Arquivo {nome_arquivo} atualizado com sucesso.')

# Agendando a coleta de notícias para rodar a cada 10 minutos
schedule.every(5).hours.do(coletar_noticias)

# Loop para manter o script rodando
while True:
    schedule.run_pending()
    time.sleep(1)