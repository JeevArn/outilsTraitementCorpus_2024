from datastructures import Film, Corpus, save_json
from analyzer import load_spacy, analyze_spacy
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm

# ouvrir le navigateur Firefox
driver = webdriver.Firefox()
# set up du temps d'attente avant de recevoir une réponse 'No Such Element Exception'
driver.implicitly_wait(10)
# ouvrir l'URL de la page web d'imdb
driver.get("https://www.imdb.com/")
# refuser les cookies
driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/div[1]/div[1]/div[2]/div[1]/button[1]").click()
# cliquer sur 'Menu'
driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/nav[1]/div[2]/label[1]").click()
# cliquer sur 'Top 250 des films'
#driver.find_element(By.XPATH, "//span[contains(text(),'Top 250 des films')]").click()
driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/nav[1]/div[2]/aside[1]/div[1]/div[2]/div[1]/div[1]/span[1]/div[1]/div[1]/ul[1]/a[2]").click()
# attendre 10 secondes pour que toute la page se charge
time.sleep(10) 

# structure en liste html : dans l'élément <ul> chaque élément <li> contient un film
# trouver l'élément <ul>
ul_films = driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/main[1]/div[1]/div[3]/section[1]/div[1]/div[2]/div[1]/ul[1]")
# trouver tous les <li> dans l'élément <ul>
elements = ul_films.find_elements(By.TAG_NAME, "li")
links=[]
for element in elements:
    # trouver le lien de chaque film
    link = element.find_element(By.TAG_NAME, "a").get_attribute("href")
    links.append(link)    

# ouvrir une nouvelle fenêtre pour ouvrir les liens (dans le cas où il y aurait plusieurs pages)
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[-1])

#print(len(links))

# initialiser le corpus
corpus=Corpus([])
for id, url in tqdm(enumerate(links), total=len(links), desc="Scraping..."):
    driver.get(url)

    id=str(id)
    # récupérer les informations du film
    title = driver.find_element(By.XPATH, "//span[@class='hero__primary-text']").text
    # récupérer le titre original s'il n'est pas le même
    try:
        og_title = driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/main[1]/div[1]/section[1]/section[1]/div[3]/section[1]/section[1]/div[2]/div[1]/div[1]").text.split(":")[-1].strip()
    except:
        og_title = title

    year = driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/main[1]/div[1]/section[1]/section[1]/div[3]/section[1]/section[1]/div[2]/div[1]/ul[1]/li[1]/a[1]").text
    ele_genres = driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/main[1]/div[1]/section[1]/section[1]/div[3]/section[1]/section[1]/div[3]/div[2]/div[1]/section[1]/div[1]/div[2]")
    genres = [a.text for a in ele_genres.find_elements(By.TAG_NAME, "a")]
    director = driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/main[1]/div[1]/section[1]/section[1]/div[3]/section[1]/section[1]/div[3]/div[2]/div[1]/section[1]/div[2]/div[1]/ul[1]/li[1]/div[1]/ul[1]/li[1]/a[1]").text
    rating = driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/main[1]/div[1]/section[1]/section[1]/div[3]/section[1]/section[1]/div[2]/div[2]/div[1]/div[1]/a[1]/span[1]/div[1]/div[2]/div[1]/span[1]").text
    synopsis = driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/main[1]/div[1]/section[1]/section[1]/div[3]/section[1]/section[1]/div[3]/div[2]/div[1]/section[1]/p[1]/span[3]").text

    # créer une instance de film
    film=Film(id, title, og_title, year, genres, director, rating, synopsis)
    # l'ajouter au corpus
    corpus.films.append(film)

driver.quit()

######## Analyser le corpus avec spacy ##########
nlp = load_spacy()
for film in corpus.films:
    analyze_spacy(nlp, film)

#print(corpus)

####### Sauvegarder le corpus en JSON ###########
save_json(corpus, "corpus_imdb.json")
