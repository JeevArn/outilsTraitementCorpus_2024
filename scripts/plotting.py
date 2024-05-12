import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
import argparse

def get_dataframe(path: str)-> DataFrame:
    """Obtenir le corpus en dataframe

    Parameters
    ----------
        path : str
            chemin du fichier json du corpus

    Returns
    -------
        DataFrame
            le corpus en dataframe
    """
    return pd.read_json(path)


def plot_flat_genre_distribution(df: DataFrame, save_path: str)-> None:
    """Obtenir le graph de distribution des genres du corpus en applatissant les listes de genres
    (càd que chaque occurrence d'un genre dans la colonne ['genres'] compte pour 1)
    
    Parameters
    ----------
        df : DataFrame 
            le corpus en dataframe obtenu avec get_dataframe
        save_path : str
            chemin d'enregistrement du graph
    
    Returns
    -------
    None
    """
    # liste applatie des genres du corpus
    genres_list = [genre for sublist in df['genres'] for genre in sublist]
    # compter les occurences de chaque genre
    genre_counts = pd.Series(genres_list).value_counts()
    # plotting
    plt.figure(figsize=(10, 6))
    genre_counts.plot(kind='bar', color='skyblue')
    plt.title('Flat Genre Distribution')
    plt.xlabel('Genres')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    #plt.show()
    plt.savefig(save_path)


def plot_grouped_genre_distribution(df: DataFrame, save_path: str)-> None:
    """Obtenir le graph de distribution des genres du corpus en regroupant les listes de genres
    (chaque combinaison de genre (peu importe l'ordre) est une catégorie)

    Parameters
    ----------
        df : DataFrame
            le corpus en dataframe obtenu avec get_dataframe
        save_path : str
            chemin d'enregistrement du graph

    Returns
    -------
    None
    """
    # convertion des liste de genres en frozenset pour ignorer l'ordre
    df['genres_frozenset'] = df['genres'].apply(frozenset)
    # compter les occurences de chaque set de genre
    genre_counts = df['genres_frozenset'].value_counts()
    # plotting
    plt.figure(figsize=(20, 6))
    genre_counts.plot(kind='bar', color='teal')
    plt.title('Grouped Genre Distribution')
    plt.xlabel('Genres')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    #plt.show()
    plt.savefig(save_path)


def plot_1st_genre_distribution(df: DataFrame, save_path: str)-> None:
    """Obtenir le graph de distribution du premier genre des films du corpus
    (seul le premier genre dans la liste pour chaque film est conservé, on considère qu'il s'agit du plus important)

    Parameters
    ----------
        df : DataFrame
            le corpus en dataframe obtenu avec get_dataframe
        save_path : str
            chemin d'enregistrement du graph

    Returns
    -------
    None
    """
    # extraire le premier genre de chaque liste de genres
    first_genres = df['genres'].apply(lambda x: x[0])
    # compter les occurences de chaque genre premier
    genre_counts = first_genres.value_counts()
    # plotting
    plt.figure(figsize=(10, 6))
    genre_counts.plot(kind='bar', color='lightcoral')
    plt.title('Genre Distribution (First Genre Only)')
    plt.xlabel('Genres')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    #plt.show()
    plt.savefig(save_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, default='data/corpus_imdb.json')
    args = parser.parse_args()
    
    df = get_dataframe(args.path)

    plot_flat_genre_distribution(df, 'plots/flat_genre_distribution.png')
    plot_grouped_genre_distribution(df, 'plots/grouped_genre_distribution.png')
    plot_1st_genre_distribution(df, 'plots/1st_genre_distribution.png')

if __name__ == '__main__':
    main()
