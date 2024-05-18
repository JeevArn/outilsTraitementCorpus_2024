"""
Module pour faire le split train/test/dev du corpus

commande complète : 
    python3 split_dataset.py --path-corpus data/raw/corpus_imdb.json --path-save data/split/
commande avec les path par défaut :
    python3 split_dataset.py
"""
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(file_path):
    """Charge les données à partir d'un fichier JSON en DataFrame
    
    Parameters
    ----------
    file_path : str
        chemin vers le fichier JSON
    
    Returns
    -------
    DataFrame
        données chargées sous forme de DataFrame
    """
    return pd.read_json(file_path)

def preprocess_data(df):
    """Prétraite les données en supprimant les colonnes inutiles, 
    en supprimant les doublons de synopsis, 
    en conservant uniquement le genre principale de chaque film
    et en filtrant les genres avec moins de 20 films
    
    Parameters
    ----------
    df : DataFrame
        le DataFrame contenant les données brutes
    
    Returns
    -------
    DataFrame
        le DataFrame prétraité
    """
    # Supprimer les colonnes inutiles
    df = df.drop(['title', 'og_title', 'year', 'director', 'rating'], axis=1)
    # Supprimer les doublons
    df = df.drop_duplicates(subset=['synopsis'])
    # Conserver uniquement le premier genre
    df['genres'] = df['genres'].apply(lambda x: x[0])
    # Supprimer les genres ayant moins de 20 films
    genre_counts = df['genres'].value_counts()
    underrep_genres = genre_counts[genre_counts < 20].index.tolist()
    df = df[~df['genres'].isin(underrep_genres)]
    return df

def split_data(df):
    """Divise les données en train, test et dev
    
    Parameters
    ----------
    df : DataFrame
        le DataFrame contenant les données prétraités à diviser
    
    Returns
    -------
    train_df : DataFrame
        Ensemble d'entraînement
    test_df : DataFrame
        Ensemble de test
    dev_df : DataFrame
        Ensemble de développement
    """
    # Diviser le DataFrame en ensembles d'entraînement et restants
    train_df, remaining = train_test_split(df,
                                           test_size=0.3,
                                           random_state=42,
                                           stratify=df['genres'],
                                           shuffle=True)
    # Diviser les données restantes en ensembles de test et de développement
    test_df, dev_df = train_test_split(remaining,
                                       test_size=0.5,
                                       random_state=42,
                                       stratify=remaining['genres'],
                                       shuffle=True)
    return train_df, test_df, dev_df

def save_data(df, file_path):
    """Enregistre le DataFrame en tant que fichier JSON
    
    Parameters
    ----------
    df : DataFrame
        Le DataFrame à enregistrer
    file_path : str
        Chemin vers le fichier JSON de sortie
    """
    df.to_json(file_path, orient="records", lines=True)

def main():
    """
    main
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--path-corpus',
                        type=str,
                        default='data/raw/corpus_imdb.json',
                        help='chemin du fichier corpus JSON')
    parser.add_argument('--path-save',
                        type=str,
                        default='data/split/',
                        help='chemin du dossier pour enregistrer les datasets')
    args = parser.parse_args()

    # Charger les données
    df = load_data('data/raw/corpus_imdb.json')
    print("Taille du corpus initial :", len(df))

    # Prétraiter les données
    df = preprocess_data(df)
    print("Taille du corpus filtré :", len(df))
    print("Nombre de genres (labels) :", df['genres'].nunique())
    print()

    # Diviser les données
    train_df, test_df, dev_df = split_data(df)
    print("Taille du split train :", len(train_df))
    print("Taille du split test :", len(test_df))
    print("Taille du split dev :", len(dev_df))

    # Enregistrer les datasets
    save_data(train_df, args.path_save + "train_dataset_imdb.json")
    save_data(test_df, args.path_save + "test_dataset_imdb.json")
    save_data(dev_df, args.path_save + "dev_dataset_imdb.json")

if __name__ == "__main__":
    main()
