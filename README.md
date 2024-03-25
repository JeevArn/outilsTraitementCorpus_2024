# outilsTraitementCorpus_2024
Projet de constitution/exploitation de corpus dans le cadre du cours d'Outils de traitement de Corpus - PluriTAL

- Tâche : classification d'url -> sites légitimes ou sites de pishing
- Corpus qui répond à cette tâche : 
    - ealvaradob/phishing-dataset (https://huggingface.co/datasets/ealvaradob/phishing-dataset)
- À quel type de prédiction peut servir ce corpus :
    - détection de pishing par classification
- À quel modèle il a servi :
    - a été utilisé pour entrainer BERT sur la détection de phishing (dataset: combined_reduced.json)
- Informations sur le corpus :

| Type | Taille | Champs | Langue | Méthode d'obtention |
| ---- | ------- | ----| ----- | ------------------- |
| email | 18,000 | text, label |en | généré par Enron Corporation |
| sms | 5,971 | text, label | en | conversion d'images obtenu sur Internet en texte avec Python |
| url | 800,000 | text, label | en | JPCERT website (Kaggle dataset existant), Github repositories where the URLs are updated once a year, open source databases including Excel files |
| sites | 80,000 | text, label | en | Collecte des données légitimes : Une recherche par mots-clés simple sur le moteur de recherche Google a été utilisée et les cinq premières URL de chaque recherche ont été collectées. Des restrictions de domaine ont été appliquées et un maximum de dix collectes à partir d'un même domaine a été imposé pour garantir une diversité dans la collection finale. Près de 25 ,874 URL actives ont été collectées à partir du référentiel de Ebbu2017 (Phishing Dataset repository). Collecte des données de phishing : PhishTank, OpenPhish et PhishRepo.|

Créateur du corpus : ealvaradob
