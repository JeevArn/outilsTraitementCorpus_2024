"""
Module principale

commande complète :
    python3 src/main.py --path-corpus data/raw/corpus_imdb.json --plot --path-plot plots/

commande avec les paths par défaut :
    python3 src/main.py

commande avec les paths par défaut et avec le plotting :
    python3 src/main.py --plot
"""
import argparse
from scrape_imdb import IMDBScraper
from datastructures import save_json
from analyzer import load_spacy, analyze_spacy
from plotting import Plotter

def main():
    """
    Main
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
    parser.add_argument('--plot', action='store_true')
    args = parser.parse_args()

    # Scraping
    scraper = IMDBScraper()
    imdb_url = "https://www.imdb.com/"
    links = scraper.scrape_links(imdb_url)
    corpus_imdb = scraper.scrape_metadata(links)

    # Analyser le corpus avec spacy
    nlp = load_spacy()
    for film in corpus_imdb.films:
        analyze_spacy(nlp, film)

    # Sauvegarder le corpus en JSON
    save_json(corpus_imdb, args.path_corpus)

    # Plotting
    if args.plot :
        plotter = Plotter(args.path_corpus, args.path_plot)
        plotter.all_plots()

if __name__ == "__main__":
    main()
