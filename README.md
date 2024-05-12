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

    - champs :
        - id : int
        - movie_name : str
        - synopsis : str
        - genre : str

    - taille du corpus :
        - train set : 7.16 MB
        - test set : 4.74 MB
    
    - format du corpus : .parquet

Créateur du corpus : datadrivenscience/