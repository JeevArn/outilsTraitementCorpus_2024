from datastructures import Token, Sentence, Film
from spacy.language import Language

def load_spacy():
    import spacy
    return spacy.load("fr_core_news_lg")

def analyze_spacy(nlp: Language, film: Film)-> None:
    """Pos-tagging du synopsis du film avec spaCy et stockage dans l'attribut analysis de la classe Film

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
