from transformers import AutoTokenizer, AutoModel
import torch

def get_embeddings(strings: list[str], layer: int = -1) -> torch.tensor:

    tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-560m")
    model = AutoModel.from_pretrained("bigscience/bloom-560m")

    inputs = tokenizer(strings, return_tensors="pt", padding=True)

    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)

    hidden_states = outputs.hidden_states[layer]

    # last_hidden_state = outputs.last_hidden_state  # shape: [batch, sequence, hidden_size]

    # To get a single embedding per sentence, you can use:
    # [CLS] token if available, or mean pooling over all tokens
    sentence_embedding = hidden_states.mean(dim=1)


    return sentence_embedding


def get_roll_embeddings(strings: list[str], window_size: int = 3, layer: int = -1):

    roll_tokens = []
    roll = 3
    for i in range(len(strings)):
        if i + roll >= len(strings):
            idx = len(strings)
        else:
            idx = i + roll
        roll_tokens.append(' '.join(strings[i:idx]))

    return get_embeddings(roll_tokens)