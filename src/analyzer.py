"""Module pour le pos-tagging su corpus"""
import spacy
from spacy.language import Language
from datastructures import Token, Sentence, Film

def load_spacy()-> Language:
    """Charger le modèle de langue spaCy

    Returns
    -------
    Language
        modèle de langue spaCy
    """
    return spacy.load("fr_core_news_lg")

def analyze_spacy(nlp: Language, film: Film)-> None:
    """Pos-tagging du synopsis du film avec spaCy 
    et stockage dans l'attribut analysis de la classe Film

    Parameters
    ----------
    nlp : Language
        modèle de langue spaCy, loading avec spacy.load()
    film : Film
        une instance de la classe Film (qui contient le synopsis du film)

    Returns
    -------
    None 
        modifie directement l'objet par référence et non pas par copie donc pas besoin de return
    """
    result=nlp(film.synopsis)
    film.analysis=[Sentence(
        tokens=[Token(
            text=token.text,
            lemma=token.lemma_,
            pos=token.pos_
        ) for token in sent]
    ) for sent in result.sents]
