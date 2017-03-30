from config import config
from data_utils import CoNLLDataset, get_vocabs, UNK, NUM, \
    get_glove_vocab, write_vocab, load_vocab, get_char_vocab, \
    export_trimmed_glove_vectors, get_processing_word


def build_data(config):
    """
    Procedure to build data

    Args:
        config: defines attributes needed in the function
    Returns:
        creates vocab files from the datasets
        creates a npz embedding file from trimmed glove vectors
    """
    processing_word = get_processing_word(lowercase=config.lowercase)

    dev   = CoNLLDataset(config.dev_filename, processing_word)
    test  = CoNLLDataset(config.test_filename, processing_word)
    train = CoNLLDataset(config.train_filename, processing_word)

    vocab_words, vocab_tags = get_vocabs([dev])
    vocab_glove = get_glove_vocab(config.glove_filename)

    vocab = vocab_words & vocab_glove
    vocab.add(UNK)
    vocab.add(NUM)

    write_vocab(vocab, config.words_filename)
    write_vocab(vocab_tags, config.tags_filename)

    vocab = load_vocab(config.words_filename)
    export_trimmed_glove_vectors(vocab, config.glove_filename, 
                                config.trimmed_filename, config.dim)

    train = CoNLLDataset(config.train_filename)
    vocab_chars = get_char_vocab(train)
    write_vocab(vocab_chars, config.chars_filename)

if __name__ == "__main__":
    build_data(config)