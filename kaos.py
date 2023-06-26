import json
import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def run_bot():
    # Instancier le navigateur Chrome
    browser = webdriver.Chrome()

    # Charger la page Web
    browser.get("https://nvd.nist.gov/")

    # Attendre que les éléments soient présents
    wait = WebDriverWait(browser, 10)

    elem_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#latestVulns")))

    items = elem_list.find_elements(By.CSS_SELECTOR, '#latestVulns > li')

    # Créer une liste pour stocker les informations
    data = []

    # Parcourir chaque élément de vulnérabilité
    for item in items:
        # Récupérer le texte de la première colonne
        cve_title = item.find_element(By.XPATH, ".//div[contains(@class, 'col-lg-9')]/p/strong/a").text
        # Exclure les numéros de CVE dans le titre
        title = item.text.split('\n')[0].replace(cve_title, '').strip()

        try:
            # Récupérer l'élément contenant la date de publication
            published_element = item.find_element(By.XPATH, ".//div[contains(text(), 'Published')]/following-sibling::div")
            published_date = published_element.text

        except NoSuchElementException:
            published_date = "N/A"

        # Récupérer le lien de la CVE pour plus de détails
        link_element = item.find_element(By.XPATH, ".//div[contains(@class, 'col-lg-9')]/p/strong/a")
        link = link_element.get_attribute('href')

        # Récupérer le texte de la deuxième colonne
        severity_score = item.find_element(By.XPATH, ".//div[contains(@class, 'col-lg-3')]/p/span/a").text

        # Créer un dictionnaire pour stocker les informations de chaque vulnérabilité
        vulnerability = {
            "Identifier": cve_title,
            "Title": title,
            "Published": published_date,
            "Severity Score": severity_score,
            "Detail": link
        }

        # Ajouter le dictionnaire à la liste des données
        data.append(vulnerability)

    # Enregistrer les données dans un fichier JSON
    with open("vulnerabilities.json", "w") as file:
        json.dump(data, file, indent=4)

    # Fermer le navigateur
    browser.quit()

# Définir l'heure à laquelle le bot doit s'exécuter
schedule.every(3).seconds.do(run_bot)

while True:
    # Vérifier si une tâche doit être exécutée
    schedule.run_pending()
    time.sleep(1)
