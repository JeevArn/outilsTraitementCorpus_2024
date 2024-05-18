# outilsTraitementCorpus_2024
Projet de constitution/exploitation de corpus dans le cadre du cours d'Outils de traitement de Corpus - PluriTAL

## Corpus de référence
- Tâche : classification de synopsis de films en fonction du genre
- Corpus qui répond à cette tâche : 
    - datadrivenscience/movie-genre-prediction (https://huggingface.co/datasets/datadrivenscience/movie-genre-prediction)
- À quel type de prédiction peut servir ce corpus :
    - prédiction du genre d'un synopsis donné
- À quel modèle il a servi :
    - a été utilisé pour une version fine-tuné de GPT2 (arnabdhar/GPT2-genre-detection)
    - et pour Ammok/movie-genre-classification

- Informations sur le corpus :
    - langue : anglais

    - champs :
        - id : int
        - movie_name : str
        - synopsis : str
        - genre : str

    - taille du corpus :
        - train set : 7.16 MB
        - test set : 4.74 MB
    
    - format du corpus : .parquet (s'apparente à un .csv compressé, permet de stocker des gros volumes de données)

Créateur du corpus : datadrivenscience/

## Création du nouveau corpus
- scraping du site d'IMDB avec selenium
- création de dataclass pour stocker les données
- sérialisation en JSON
- plotting du corpus obtenu avec 6 figures disponibles dans plots/
- suppression des genres trop peu dotés (si n<20) + suppression des colonnes inutiles
- split en train/test/dev
- création de la carte YAML du dataset

## Instructions pour reproduire le dataset
- cloner le dépôt
- lancer main.py
- puis lancer split_dataset.py

- s'assurer d'avoir un dossier data/ contenant les dossiers raw/ et split/ pour pouvoir lancer les commandes avec les paths par défauts
- s'assurer d'avoir installé tous les requirements (voir requirements.txt)

- vous obtiendrez ainsi :
    - les datasets dans data/
    - les plots dans plots/
