"""Module permettant de scraper le site imdb"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm
from datastructures import Film, Corpus

class IMDBScraper:
    """Classe permettant de scraper le site imdb

    Attributes
    ----------
    driver : selenium.webdriver.firefox.webdriver.WebDriver
        Selenium WebDriver utilisé pour le scraping
        
    Methods
    -------
    scrape_links(page):
        collecter les liens vers chaque film de la page du Top 250
        
    scrape_metadata(links):
        collecter les métadonnées de chaque film et les stocker dans un Corpus
    """
    def __init__(self):
        self.driver = self._set_driver()

    def _set_driver(self):
        """Set up du driver Selenium avec Firefox
        
        Returns
        -------
        driver : selenium.webdriver.firefox.webdriver.WebDriver
            driver configuré
        """
        # mode headless pour ne pas afficher le navigateur
        options = Options()
        options.headless = True
        # navigateur Firefox
        driver = webdriver.Firefox()
        # set up du temps d'attente avant de recevoir une réponse 'No Such Element Exception'
        driver.implicitly_wait(10)
        return driver

    def scrape_links(self, page):
        """Collecter les liens vers chaque film de la page

        Parameters
        ----------
        page : str
            lien de la page d'acceuil d'imdb

        Returns
        -------
        links : list
            liste des liens vers chaque film
        """
        driver = self.driver

        # ouvrir l'URL de la page web d'imdb
        driver.get(page)
        # refuser les cookies
        driver.find_element(
            By.XPATH,
            "/html[1]/body[1]/div[2]/div[1]/div[1]/div[2]/div[1]/button[1]"
            ).click()
        # cliquer sur 'Menu'
        driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/nav[1]/div[2]/label[1]").click()
        time.sleep(1)
        # cliquer sur 'Top 250 des films'
        driver.find_element(
            By.XPATH,
            "/html[1]/body[1]/div[2]/nav[1]/div[2]/aside[1]/div[1]/div[2]/div[1]/div[1]/span[1]/div[1]/div[1]/ul[1]/a[2]"
            ).click()
        # attendre 5 secondes pour que toute la page se charge
        time.sleep(5)
        # structure en liste html : dans l'élément <ul> chaque élément <li> contient un film
        # trouver l'élément <ul>
        ul_films = driver.find_element(
            By.XPATH, 
            "/html[1]/body[1]/div[2]/main[1]/div[1]/div[3]/section[1]/div[1]/div[2]/div[1]/ul[1]"
            )
        # trouver tous les <li> dans l'élément <ul>
        elements = ul_films.find_elements(By.TAG_NAME, "li")
        # trouver le lien de chaque film et le mettre dans une liste
        links = [element.find_element(By.TAG_NAME, "a").get_attribute("href") for element in elements]
        return links


    def scrape_metadata(self, links):
        """Collecter les métadonnées de chaque film et les mettre dans le Corpus

        Parameters
        ----------
        page : str
            lien de la page d'acceuil d'imdb

        Returns
        -------
        corpus : Corpus
            un objet Corpus qui contient les instances de Film avec les métadonnées scrapées
        """
        driver = self.driver

        # initialiser le corpus
        corpus=Corpus([])

        #for i, url in tqdm(enumerate(links[:20]), total=len(links[:20]), desc="Scraping..."): # limite à 20 pour tester
        for i, url in tqdm(enumerate(links), total=len(links), desc="Scraping..."):
            driver.get(url)

            id_film=str(i)
            # récupérer les informations du film
            title = driver.find_element(By.XPATH, "//span[@class='hero__primary-text']").text
            # récupérer le titre original s'il n'est pas le même
            try:
                og_title = driver.find_element(
                    By.XPATH,
                    "/html[1]/body[1]/div[2]/main[1]/div[1]/section[1]/section[1]/div[3]/section[1]/section[1]/div[2]/div[1]/div[1]"
                    ).text.split(":")[-1].strip()
            except: # NoSuchElementException et ElementNotInteractableException ne fonctionnaient pas donc on garde juste except
                og_title = title

            year = driver.find_element(
                By.XPATH,
                "/html[1]/body[1]/div[2]/main[1]/div[1]/section[1]/section[1]/div[3]/section[1]/section[1]/div[2]/div[1]/ul[1]/li[1]/a[1]"
                ).text
            ele_genres = driver.find_element(
                By.XPATH,
                "/html[1]/body[1]/div[2]/main[1]/div[1]/section[1]/section[1]/div[3]/section[1]/section[1]/div[3]/div[2]/div[1]/section[1]/div[1]/div[2]"
                )
            genres = [a.text for a in ele_genres.find_elements(By.TAG_NAME, "a")]
            director = driver.find_element(
                By.XPATH,
                "/html[1]/body[1]/div[2]/main[1]/div[1]/section[1]/section[1]/div[3]/section[1]/section[1]/div[3]/div[2]/div[1]/section[1]/div[2]/div[1]/ul[1]/li[1]/div[1]/ul[1]/li[1]/a[1]"
                ).text
            rating = driver.find_element(
                By.XPATH,
                "/html[1]/body[1]/div[2]/main[1]/div[1]/section[1]/section[1]/div[3]/section[1]/section[1]/div[2]/div[2]/div[1]/div[1]/a[1]/span[1]/div[1]/div[2]/div[1]/span[1]"
                ).text
            synopsis = driver.find_element(
                By.XPATH,
                "/html[1]/body[1]/div[2]/main[1]/div[1]/section[1]/section[1]/div[3]/section[1]/section[1]/div[3]/div[2]/div[1]/section[1]/p[1]/span[3]"
                ).text

            # créer une instance de film
            film_instance=Film(id_film, title, og_title, year, genres, director, rating, synopsis)
            # l'ajouter au corpus
            corpus.films.append(film_instance)

        driver.quit()
        return corpus
