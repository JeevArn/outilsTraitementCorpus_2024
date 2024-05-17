"""
Module permettant d'effectuer le plotting
utilisable seul sur le corpus déjà constitué

commande complète : 
    python3 src/plotting.py --path <path_to_corpus> --save_path <path_to_save_plots>

commande avec les paths par défaut :
    python3 src/plotting.py
"""
import argparse
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
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
        plt.savefig(self.path_plot + 'flat_genre_distribution.png')


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


    def plot_avg_token_per_genre(self, df: DataFrame) -> None:
        """Créer un graphique de la moyenne du nombre de tokens des synopsis par genre

        Parameters
        ----------
        df : DataFrame
            Le corpus en dataframe obtenu avec get_dataframe
        
        Returns
        -------
        None
        """
        # calculer le nombre de tokens pour chaque synopsis en utilisant split()
        df['num_tokens'] = df['synopsis'].apply(lambda x: len(str(x).split()))
        # exploser la colonne 'genres' pour obtenir une ligne par genre et film
        df_exploded = df.explode('genres')
        # calculer la moyenne du nombre de tokens par genre
        avg_tokens_per_genre = df_exploded.groupby('genres')['num_tokens'].mean()
        # plotting
        plt.figure(figsize=(10, 6))
        avg_tokens_per_genre.plot(kind='bar', color='mediumseagreen')
        plt.title('Average Number of Tokens per Genre')
        plt.xlabel('Genres')
        plt.ylabel('Average Number of Tokens')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(self.path_plot + 'avg_token_per_genre.png')


    def plot_avg_token_per_1st_genre(self, df: DataFrame) -> None:
        """Créer un graphique de la moyenne du nombre de tokens des synopsis par genre
        en ne prenant en compte que le premier genre de chaque film

        Parameters
        ----------
        df : DataFrame
            Le corpus en dataframe obtenu avec get_dataframe
        
        Returns
        -------
        None
        """
        # calculer le nombre de tokens pour chaque synopsis en utilisant split()
        df['num_tokens'] = df['synopsis'].apply(lambda x: len(str(x).split()))
        # prendre uniquement le premier genre de chaque liste de genres
        df['first_genre'] = df['genres'].apply(lambda x: x[0])
        # calculer la moyenne du nombre de tokens par premier genre
        avg_tokens_per_1st_genre = df.groupby('first_genre')['num_tokens'].mean()
        # plotting
        plt.figure(figsize=(10, 6))
        avg_tokens_per_1st_genre.plot(kind='bar', color='green')
        plt.title('Average Number of Tokens per First Genre')
        plt.xlabel('First Genre')
        plt.ylabel('Average Number of Tokens')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(self.path_plot + 'avg_token_per_1st_genre.png')


    def plot_zipf_law(self, df: pd.DataFrame) -> None:
        """Appliquer la loi de Zipf sur le corpus et tracer le graphique

        Parameters
        ----------
        df : DataFrame
            Le corpus en dataframe obtenu avec get_dataframe
        
        Returns
        -------
        None
        """
        # combiner tous les synopsis en une seule grande chaîne de caractères
        all_synopsis = " ".join(df['synopsis'].tolist()).lower()
        # tokeniser les mots (split sur les espaces)
        tokens = all_synopsis.split()
        # compter les fréquences des mots
        word_counts = Counter(tokens)
        # trier les mots par fréquence décroissante
        sorted_word_counts = word_counts.most_common()
        # extraire les fréquences
        frequencies = [count for word, count in sorted_word_counts]
        # calculer les rangs
        ranks = np.arange(1, len(frequencies) + 1)
        # plotting
        plt.figure(figsize=(10, 6))
        plt.loglog(ranks, frequencies, marker=".")
        plt.title("Loi de Zipf sur les synopsis")
        plt.xlabel("Rang")
        plt.ylabel("Fréquence")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(self.path_plot + 'zipf_law.png')

    def all_plots(self):
        """
        Obtenir tous les plots disponibles
        """
        df = self.get_dataframe()
        self.plot_flat_genre_distribution(df)
        self.plot_grouped_genre_distribution(df)
        self.plot_1st_genre_distribution(df)
        self.plot_avg_token_per_genre(df)
        self.plot_avg_token_per_1st_genre(df)
        self.plot_zipf_law(df)


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
    plotter.all_plots()
    print('Plotting effectué !')

if __name__ == '__main__':
    main()
