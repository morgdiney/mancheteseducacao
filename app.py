import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def coletar_noticias():
    url = "https://g1.globo.com/educacao/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        noticias = soup.find_all("a", class_="feed-post-link")

        if not noticias:
            print(" Nenhuma notícia encontrada. Verifique a estrutura do site.")
            return

        dados = {"Manchete": [noticia.text.strip() for noticia in noticias]}
        df = pd.DataFrame(dados)

        nome_arquivo = f"manchetes_noticias.csv"
        df.to_csv(nome_arquivo, index=False, encoding="utf-8")
        print(f"Dados salvos com sucesso em {nome_arquivo}!")

    else:
        print(f"Erro ao acessar a página: {response.status_code}")

# Executa a função
coletar_noticias()