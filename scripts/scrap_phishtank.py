from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# liste pour stocker les liens de phishing
is_online_phish = []

# ouvrir le navigateur Firefox
driver = webdriver.Firefox()

# ouvrir l'URL de PhishTank et cliquer sur 'Phish Search'
driver.get("https://phishtank.org")
driver.find_element(By.XPATH, "//a[contains(text(),'Phish Search')]").click()

# cliquer sur 'Valid phishes' dans le form 'Valid?'
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//select[@name='valid']"))) # <select name="valid" xpath="1"></select>
select = Select(element)
select.select_by_value("y") # <option value="y">Online</option>
selected_option = select.first_selected_option
selected_option.click()

# cliquer sur 'Online' dans le form 'Online?'
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//select[@name='active']"))) # <select name="active" xpath="1"></select>
select = Select(element)
select.select_by_value("y") # <option value="y">Online</option>
selected_option = select.first_selected_option
selected_option.click()

# cliquer sur 'Search'
search_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Search']")
search_button.click()

# boucler sur les pages de résultats
while True:

    if len(is_online_phish) > 200: 
    # enlever cette condition si vous voulez récupérer tous les liens de phishing valides de PhishTank
        break

    # récupérer les liens de la première colonne du tableau
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//td[@class='value']/a[contains(@href, 'phish_id')]")))
    links = driver.find_elements(By.XPATH, "//td[@class='value']/a[contains(@href, 'phish_id')]")
    link_urls = [link.get_attribute("href") for link in links]

    # ouvrir une nouvelle fenêtre pour ouvrir les liens
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])

    # ouvrir chaque lien dans la nouvelle fenêtre et récupérer le vrai lien de phishing
    for url in link_urls:
        driver.get(url)
        phishing_link_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/div[3]/span[1]/b[1]")))
        phishing_link = phishing_link_element.text

        # si le lien de phishing n'est pas déjà dans la liste is_online_phish, on l'ajoute
        if phishing_link not in is_online_phish:
            is_online_phish.append(phishing_link)
    
    driver.close() # fermer la fenêtre
    driver.switch_to.window(driver.window_handles[0]) # retourner à la fenêtre principale

    try:
        # passer à la page suivante
        next_page = driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr[22]/td[5]/b[1]/a[1]")
        next_page.click()
    except:
        print("no more next page")
        break # sortir de la boucle si aucune page suivante n'est disponible
                              
driver.quit() # fermer le navigateur

print("phishing links count:", len(is_online_phish))
print("10 first:")
for i in is_online_phish[:10]:
    print(i)
print()

with open("is_online_phish.txt", "w") as f:
    for link in is_online_phish:
        f.write(link + "\n")
print()

print("phishing links saved to is_online_phish.txt")
