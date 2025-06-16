from flair.data import Sentence
from flair.models import SequenceTagger
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification


def get_pos(tokens_list: list[str]) -> dict[str: str]:

    sentence_str = ' '.join(tokens_list)

    tagger = SequenceTagger.load("flair/upos-multi")

    sentence = Sentence(sentence_str)

    # predict POS tags
    tagger.predict(sentence)

    # iterate over tokens and print the predicted POS label
    """print("The following POS tags are found:")
    for token in sentence:
        print(token.get_label("upos"))"""

    return [(token.text, token.tag) for token in sentence]


def get_pos_2(original_tokens: list[str]):
    sentence_str = ' '.join(original_tokens)
    tagger = SequenceTagger.load("flair/upos-multi")
    sentence = Sentence(sentence_str)
    tagger.predict(sentence)
    flair_tokens = [token.text for token in sentence]
    flair_tags = [token.get_label('upos').value for token in sentence]

    # Merge flair tokens to match original tokens
    result = []
    i = 0  # index for original_tokens
    j = 0  # index for flair_tokens
    while i < len(original_tokens) and j < len(flair_tokens):
        otok = original_tokens[i]
        ftok = flair_tokens[j]
        # If token matches exactly, take POS
        if otok == ftok:
            result.append((otok, flair_tags[j]))
            i += 1
            j += 1
        # Else, try to merge flair tokens to reconstruct original token
        else:
            merged = ftok
            tags = [flair_tags[j]]
            j += 1
            while j < len(flair_tokens) and merged + flair_tokens[j] in otok:
                merged += flair_tokens[j]
                tags.append(flair_tags[j])
                j += 1
            # Check if we have reconstructed the original token
            if merged == otok:
                result.append((otok, tags[0]))  # Take the first tag, or handle as needed
            else:
                result.append((otok, 'X'))  # Tag as unknown if unable to reconstruct
            i += 1
    # Pad remaining original tokens if any
    while i < len(original_tokens):
        result.append((original_tokens[i], 'X'))
        i += 1
    return result


def get_ner(token_list: list[str]) -> tuple[dict[str: str], dict[str: str]]:

    tokenizer = AutoTokenizer.from_pretrained('Babelscape/wikineural-multilingual-ner')
    model = AutoModelForTokenClassification.from_pretrained('Babelscape/wikineural-multilingual-ner')

    nlp = pipeline('ner', model=model, tokenizer=tokenizer, grouped_entities=True)

    sentence_str = ' '.join(token_list)

    ner = nlp(sentence_str)

    tags = ['0'] * len(token_list)
    idx = 0
    offsets = []
    for word in token_list:
        start = sentence_str.find(word, idx)
        offsets.append((start, start + len(word)))
        idx = start + len(word)

    for ent in ner:
        for i, (start, end) in enumerate(offsets):
            if start >= ent['start'] and end <= ent['end']:
                tags[i] = ent['entity_group']

    return [(token_list[i], tags[i]) for i in range(len(token_list))], [(tok['word'], tok['entity_group']) for tok in ner]


if __name__ == '__main__':
    print(get_ner('Hi my name is Nizar Michaud and I live in Switzerland Lausanne'.split(' ')))
