# Functionality to load the dataset
# We will be working with restaurant reviews in Las Vegas.

import numpy as np
from collections import Counter
from typing import List, Sequence, Tuple, Dict
from numpy.typing import NDArray

UNKNOWN = '_unk'

def load_data(path: str = 'task03_data.npy') -> Tuple[List[List[str]]]:
    """Loads the dataset and returns 1-star and 5-star reviews.

    Args:
        path (str, optional): Path to the dataset. Defaults to 'task03_data.npy'.

    Returns:
        List[List[str]]: 1-star reviews
        List[List[str]]: 5-star reviews
    """
    data = np.load(path, allow_pickle=True).item()
    reviews_1_star = [[token.lower() for token in sequence] for sequence in data['reviews_1star']]
    reviews_5_star = [[token.lower() for token in sequence] for sequence in data['reviews_5star']]
    return reviews_1_star, reviews_5_star
    
def build_vocabulary(corpus: List[List[str]]) -> Tuple[List[List[str]], Tuple[str], Tuple[int]]:
    """Builds the vocabulary and counts how often each token occurs. Also adds a token for uncommon words, UNKNOWN. 

    Args:
        corpus (List[List[str]]): All sequences in the dataset

    Returns:
        List[List[str]]: All sequences in the dataset, where infrequent tokens are replaced with UNKNOWN
        Tuple[str]: All unique tokens in the dataset
        Tuple[int]: The frequency of each token
    """
    corpus_flattened = [token for sequence in corpus for token in sequence]
    vocabulary, counts = zip(*Counter(corpus_flattened).most_common(200))
    # filter the corpus for the most common words
    corpus = [[token if token in vocabulary else UNKNOWN for token in sequence] for sequence in corpus]
    vocabulary += (UNKNOWN, )
    counts += (sum([token == UNKNOWN for sequence in corpus for token in sequence]),)
    return corpus, vocabulary, counts

def compute_token_to_index(vocabulary: Tuple[str], counts: Tuple[int]) -> Tuple[Dict[str, int], Dict[int, str]]:
    """Computes a mapping from tokens in the vocabulary to integeres and vice versa. 

    Args:
        vocabulary (Tuple[str]): All unique tokens in the vocabulary
        counts (Tuple[int]): How often each token appears

    Returns:
        Dict[str, int]: A mapping from token to its unique index
        Dict[int, str]: The inverse mapping from index to token
        Dict[int, int]: Mapping from unique token index to count
    """
    ###########################
    # YOUR CODE HERE
    token_to_index = {token: index for index, token in enumerate(vocabulary)}
    index_to_token = {index: token for token, index in token_to_index.items()}
    index_to_count = {index: count for index, count in enumerate(counts)}
    return token_to_index, index_to_token, index_to_count
    ###########################

def get_token_pairs_from_window(sequence: Sequence[str], window_size: int, token_to_index: Dict[str, int]) -> Sequence[Tuple[int, int]]:
    """ Collect all ordered token pairs from a sentence (sequence) that are at most `window_size` apart.
    Note that duplicates should appear more than once, e.g. for "to be to", (to, be) should be returned more than once, as "be"
    is in the context of both the first and the second "to".

    Args:
        sequence (Sequence[str]): The sentence to get tokens from
        window_size (int): The maximal window size
        token_to_index (Dict[str, int]): Mapping from tokens to numerical indices

    Returns:
        Sequence[Tuple[int, int]]: A list of pairs (token_index, token_in_context_index) with pairs of tokens that co-occur, represented by their numerical index.
    """
    ###########################
    # YOUR CODE HERE
    token_pairs = []
    sequence = [token_to_index[token] for token in sequence]
    for i, token in enumerate(sequence):
        for j in range(max(0, i - window_size), min(len(sequence), i + window_size + 1)):
            if i != j:
                token_pairs.append((token, sequence[j]))
    return token_pairs
    ###########################
