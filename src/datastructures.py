"""
Module qui contient les dataclass pour stocker les données récoltées
et les fonctions pour la sérialisation en JSON
"""
import json
from dataclasses import dataclass, asdict, field

# Stocker l'analyse de spacy
@dataclass
class Token:
    """
    classe qui représente un Token

    Attributes
    ----------
    text: str
    lemma: str
    pos: str
    """
    text: str
    lemma: str
    pos: str

@dataclass
class Sentence:
    """
    classe qui représente une phrase (Sentence)

    Attributes
    ----------
    tokens: list[Token]
    """
    tokens: list[Token]

# Stocker les métadonnées d'un film + l'analyse du contenu textuel
@dataclass
class Film:
    """
    classe qui représente un Film

    Attributes
    ----------
    id: str
    title: str
    og_title: str
    year: int
    genres: list[str]
    director: str
    rating: str
    synopsis: str
    analysis: list[Sentence]
    """
    id: str
    title: str
    og_title: str
    year: int
    genres: list[str]
    director: str
    rating: str
    synopsis: str
    analysis: list[Sentence] = field(default_factory=list)

# Stocker le corpus de films
@dataclass
class Corpus:
    """
    classe qui représente le Corpus de films

    Attributes
    ----------
        films: list[Film]
    """
    films: list[Film]

# Sérialisation en JSON
def save_json(corpus: Corpus, file_path: str)-> None:
    """Enregistrer le corpus en JSON

    Parameters
    ----------
    corpus : Corpus
        Le corpus de films à enregistrer
    file_path : str
        Le chemin du fichier JSON où enregistrer le corpus

    Returns
    -------
    None
    """
    data=[]
    for film in corpus.films:
        current={
            "id": film.id,
            "title": film.title,
            "og_title": film.og_title,
            "year": film.year,
            "genres": film.genres,
            "director": film.director,
            "rating": film.rating,
            "synopsis": film.synopsis,
            # un dictionnaire pour chaque phrase
            "analysis": [serialize_sentence(sentence) for sentence in film.analysis] 
        }
        data.append(current)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def serialize_sentence(sentence: Sentence) -> dict:
    """Sérialiser une instance de Sentence en dictionnaire

    Parameters
    ----------
    sentence : Sentence
        une instance de Sentence

    Returns
    -------
    dict
        un dictionnaire avec pour clé "tokens" et pour valeur une liste de dictionnaires 
        chacun contenant l'analyse d'un token
        càd {"text": "...", "lemma": "...", "pos": "..."}
    """
    return {
        "tokens": [asdict(token) for token in sentence.tokens]
    }
