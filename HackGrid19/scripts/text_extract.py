from rake_nltk import Rake
r = Rake()


def extract_tag(text):
    r.extract_keywords_from_text(text)
    tags = r.get_ranked_phrases()
    suggested_keywords = [[a,b] for a in tags for b in tags if a!=b]
    return suggested_keywords

def make_pairs(list):
    return [ a+b for a in list for b in list if a!=b ]
