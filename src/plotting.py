"""
Module permettant d'effectuer le plotting
utilisable seul sur le corpus déjà constitué

commande complète : 
    python3 src/plotting.py --path <path_to_corpus> --save_path <path_to_save_plots>

commande avec les paths par défaut :
    python3 src/plotting.py
"""
import argparse
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame

class Plotter:
    """
    Classe permettant de traiter les plots des distributions des genres du corpus

    Attributes
    ----------
    path_corpus : str
        path du fichier JSON contenant le corpus
    path_plot : str
        path du dossier de sauvegarde des plots

    Methods
    -------
    get_dataframe() -> DataFrame:
        Load le corpus en Dataframe
    plot_flat_genre_distribution() -> None:
        Plot flat genre distribution
    plot_grouped_genre_distribution() -> None:
        Plot grouped genre distribution
    plot_1st_genre_distribution() -> None:
        Plot distribution of the first genre of each film
    """

    def __init__(self, path_corpus: str, path_plot: str):
        """
        Initialiser le Plotter avec les chemins pour le corpus et le dossier de sauvegarde des plots

        Parameters
        ----------
        path_corpus : str
            path du fichier JSON contenant le corpus
        path_plot : str
            path du dossier de sauvegarde des plots
        """
        self.path_corpus = path_corpus
        self.path_plot = path_plot


    def get_dataframe(self)-> DataFrame:
        """Obtenir le corpus en dataframe

        Returns
        -------
        DataFrame
            le corpus en dataframe
        """
        return pd.read_json(self.path_corpus)


    def plot_flat_genre_distribution(self, df: DataFrame)-> None:
        """Obtenir le graph de distribution des genres du corpus
        en applatissant les listes de genres
        (càd que chaque occurrence d'un genre dans la colonne ['genres'] compte pour 1)
        
        Parameters
        ----------
        df : DataFrame 
            le corpus en dataframe obtenu avec get_dataframe
        
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
        plt.savefig(self.path_plot + 'grouped_genre_distribution.png')


    def plot_grouped_genre_distribution(self, df: DataFrame)-> None:
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
        plt.savefig(self.path_plot + 'grouped_genre_distribution.png')


    def plot_1st_genre_distribution(self, df: DataFrame)-> None:
        """Obtenir le graph de distribution du premier genre des films du corpus
        (seul le premier genre dans la liste pour chaque film est conservé, 
        on considère qu'il s'agit du plus important)

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
        plt.savefig(self.path_plot + '1st_genre_distribution.png')


def main():
    """
    main
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--path-corpus',
                        type=str,
                        default='data/raw/corpus_imdb.json',
                        help='chemin du fichier corpus JSON')
    parser.add_argument('--path-plot',
                        type=str,
                        default='plots/',
                        help='chemin du dossier pour enregistrer les plots')
    args = parser.parse_args()

    plotter = Plotter(args.path_corpus, args.path_plot)
    df = plotter.get_dataframe()
    plotter.plot_flat_genre_distribution(df)
    plotter.plot_grouped_genre_distribution(df)
    plotter.plot_1st_genre_distribution(df)
    print('Plotting effectué !')

if __name__ == '__main__':
    main()
