from bs4 import BeautifulSoup
import requests
import pandas as pd

# URL da página que queremos fazer scraping
url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

# Utilizar o Chrome como agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'

# Configurar o cabeçalho da solicitação com o user agent
headers = {'User-Agent': USER_AGENT}

# Conexão: Enviar uma solicitação GET para a URL
response = requests.get(url, headers=headers)

# Verificar se a solicitação foi bem-sucedida (status 200)
if response.status_code == 200:

    # Parse a página com o BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontre os elementos HTML que contêm os títulos de notícias
    data_title_rating = soup.find_all("div", class_="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon "
                                        "ipc-title--on-textPrimary sc-b85248f1-7 lhgKeb cli-title")

    # Encontrar a descrição que contêm: Ano de lançamento, duração e classificação etária
    data_about_movie = soup.find_all("div", class_="cli-title-metadata")

    # Encontrar quantidade de estrelas e total de votos
    data_star_rating = soup.find_all("span", class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating")

    # Pegar a posição e título
    data_movie = []

    # Separar a posição do título
    for x in data_title_rating:
        data_movie.append(x.text.split(".", 1))

    # Título
    title = []
    # Posição
    rating = []
    # Data de lançamento
    release_year = []
    # Duração do filme
    duration = []
    # Classificação etária
    age_rating = []
    # Quantidade de estrelas
    star_rating = []
    # Total de votos
    votes = []

    # Verificar se existe o data_star_rating
    if data_star_rating:
        for x in data_star_rating:
            value = x.text.split("\xa0")
            star_rating.append(value[0])
            votes.append(value[1].replace("(", "").replace(")", ""))
    else:
        print("Error: data_star_rating don't exists")

    # Verificar se existe o data_about_movie
    if data_about_movie:
        for data in data_about_movie:
            # Encontrar todos os spans dentro da div
            span = data.find_all("span")

            # Verificar se há pelo menos três spans na lista de spans
            if len(span) == 3:
                release_year.append(span[0].text)
                duration.append(span[1].text)
                age_rating.append(span[2].text)
    else:
        print("Error: data_about_movie don't exists")

    # Separar o título e a posição
    for x in data_movie:
        rating.append(x[0])
        title.append(x[1].strip())

    # Criando um dicionário para inserir no DataFrame
    d = {"rating": rating,
         "title": title,
         "release_year": release_year,
         "duration": duration,
         "age_rating": age_rating,
         "star_rating": star_rating,
         "votes": votes
         }
    df = pd.DataFrame(data=d)

    # Função para converter valores numéricos, mantendo as strings inalteradas
    def convert_to_numeric(value):
        try:
            return pd.to_numeric(value)
        except:
            return value

    # Alterando os tipos de cada objeto
    df["age_rating"] = df["age_rating"].apply(convert_to_numeric)
    df["rating"] = df["rating"].apply(convert_to_numeric)
    df["title"] = df["title"].astype(str)
    df["release_year"] = df["release_year"].apply(convert_to_numeric)
    df["duration"] = df["duration"].astype(str)
    df["star_rating"] = df["star_rating"].apply(convert_to_numeric)
    df["votes"] = df["votes"].astype(str)

    # Converter para csv e excel
    df.to_csv("IMDB.csv", encoding="utf-8-sig", sep=',', index=False)
    df.to_excel("IMDB.xlsx", index=False,  engine='openpyxl')

else:
    print("Falha ao acessar a página:", response.status_code)
