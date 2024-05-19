"""
Script pour équilibrer les classes du corpus
Ce script supprime les colonnes inutiles, 
supprime les doublons,
supprime les outliers, 
filtre les genres sous-représentés,
et utilise CamemBERT pour générer des exemples supplémentaires pour ces genres
"""
import json
from typing import List
from random import randint
import pandas as pd
from pandas import DataFrame
from transformers import pipeline
from tqdm import tqdm

def load_corpus(file_path: str) -> DataFrame:
    """
    Charger le corpus à partir d'un fichier JSON

    Parameters
    ----------
    file_path : str
        Chemin vers le fichier JSON d'entrée

    Returns
    -------
    DataFrame
        Le corpus chargé sous forme de DataFrame
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return DataFrame(data)


def clean_corpus(df: DataFrame, cols_to_keep: List[str], id_col: str) -> DataFrame:
    """
    Nettoyer le corpus en supprimant les doublons, les outliers et les colonnes inutiles

    Parameters
    ----------
    df : DataFrame
        DataFrame contenant le corpus
    cols_to_keep : List[str]
        Liste des colonnes à conserver dans la DataFrame nettoyée
    id_col : str
        Nom de la colonne identifiant les doublons

    Returns
    -------
    DataFrame
        DataFrame nettoyée
    """
    # supprimer les doublons
    df = df.drop_duplicates(subset=id_col)
    # supprimer les colonnes inutiles
    df = df[cols_to_keep]
    # conserver le premier genre comme genre principal
    df['genres'] = df['genres'].apply(lambda x: x[0] if isinstance(x, list) and x else None)
    # supprimer les outliers
    genre_counts = df['genres'].value_counts()
    underrep_genres = genre_counts[genre_counts < 20].index.tolist()
    df = df[~df['genres'].isin(underrep_genres)]
    return df


def augment_data(examples: DataFrame, fillmask, mask_token: str, text_col: str) -> List[str]:
    """
    Augmenter les données en utilisant CamemBERT pour générer des exemples supplémentaires

    Parameters
    ----------
    examples : DataFrame
        DataFrame contenant les exemples à augmenter
    fillmask : pipeline
        Pipeline de remplissage de masque
    mask_token : str
        Token de masque utilisé par le modèle
    text_col : str
        Nom de la colonne du texte (synopsis)

    Returns
    -------
    List[str]
        Liste de textes augmentés
    """
    outputs = []
    for sentence in examples[text_col]:
        words = sentence.split(' ')
        k = randint(1, len(words) - 1)
        masked_sentence = " ".join(words[:k] + [mask_token] + words[k+1:])
        try:
            predictions = fillmask(masked_sentence)
            augmented_sequences = [predictions[i]["sequence"] for i in range(3)]
            outputs += [sentence] + augmented_sequences
        except Exception as error:
            print(f"Erreur lors de la génération de texte pour la phrase: {masked_sentence}, erreur: {error}")
            outputs.append(sentence)
    return outputs


def balance_classes(df: DataFrame, genre_col: str, text_col: str, target_count: int) -> DataFrame:
    """
    Équilibrer les classes en générant des exemples supplémentaires pour les genres sous-représentés

    Parameters
    ----------
    df : DataFrame
        DataFrame contenant le corpus
    genre_col : str
        Nom de la colonne des genres
    text_col : str
        Nom de la colonne du texte (synopsis)
    target_count : int
        Nombre cible d'exemples pour chaque genre

    Returns
    -------
    DataFrame
        DataFrame avec les classes équilibrées
    """
    genres = df[genre_col].value_counts()
    minority_genres = genres[genres < target_count].index.tolist()
    fillmask = pipeline("fill-mask", model="camembert-base")
    mask_token = fillmask.tokenizer.mask_token

    new_samples = []
    for genre in minority_genres:
        samples_needed = target_count - genres[genre]
        genre_samples = df[df[genre_col] == genre]
        for _ in tqdm(range(samples_needed), desc=f"Génération d'exemples pour {genre}"):
            sample = genre_samples.sample(n=1)
            augmented_texts = augment_data(sample, fillmask, mask_token, text_col)
            for text in augmented_texts:
                new_sample = sample.copy()
                new_sample[text_col] = text
                new_samples.append(new_sample)

    new_samples_df = pd.concat(new_samples, ignore_index=True)
    df = pd.concat([df, new_samples_df], ignore_index=True)
    return df


def save_corpus(df: DataFrame, file_path: str) -> None:
    """
    Sauvegarder le corpus dans un fichier JSON

    Parameters
    ----------
    df : DataFrame
        DataFrame contenant le corpus
    file_path : str
        Chemin vers le fichier JSON de sortie

    Returns
    -------
    None
    """
    data = df.to_dict(orient='records')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main(input_file: str, output_file: str, cols_to_keep: List[str], id_col: str,
         genre_col: str, text_col: str, target_count: int) -> None:
    """
    Fonction principale pour charger, nettoyer, équilibrer et sauvegarder le corpus.

    Parameters
    ----------
    input_file : str
        Chemin vers le fichier JSON d'entrée
    output_file : str
        Chemin vers le fichier JSON de sortie
    cols_to_keep : List[str]
        Liste des colonnes à conserver dans la DataFrame nettoyée
    id_col : str
        Nom de la colonne identifiant les doublons
    genre_col : str
        Nom de la colonne des genres
    text_col : str
        Nom de la colonne du texte (synopsis)
    target_count : int
        Nombre cible d'exemples pour chaque genre

    Returns
    -------
    None
    """
    df = load_corpus(input_file)
    df = clean_corpus(df, cols_to_keep, id_col)
    df = balance_classes(df, genre_col, text_col, target_count)
    save_corpus(df, output_file)

if __name__ == "__main__":
    INPUT_FILE = "data/raw/corpus_imdb.json"
    OUTPUT_FILE = "data/process/augmented_corpus.json"
    COLS_TO_KEEP = ["id", "synopsis", "genres"]
    ID_COL = "id"
    GENRE_COL = "genres"
    TEXT_COL = "synopsis"
    TARGET_COUNT = 60

    main(INPUT_FILE, OUTPUT_FILE, COLS_TO_KEEP, ID_COL, GENRE_COL, TEXT_COL, TARGET_COUNT)
