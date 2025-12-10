"""Stop words utility for filtering common words from text analysis."""

# Common English stop words to filter out during keyword extraction
ENGLISH_STOP_WORDS = {
    # Articles
    "a", "an", "the",
    # Pronouns
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them",
    "my", "your", "his", "her", "its", "our", "their", "mine", "yours", "hers", "ours", "theirs",
    # Prepositions
    "in", "on", "at", "by", "for", "with", "from", "to", "of", "about", "into", "onto",
    "through", "during", "before", "after", "above", "below", "up", "down", "out", "off",
    "over", "under", "again", "further", "then", "once",
    # Conjunctions
    "and", "or", "but", "if", "because", "as", "until", "while", "whereas", "since",
    # Common verbs (basic forms)
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having",
    "do", "does", "did", "doing", "will", "would", "should", "could", "may", "might",
    "can", "cannot", "must", "shall",
    # Common adjectives/adverbs
    "this", "that", "these", "those", "all", "each", "every", "both", "few", "more",
    "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same",
    "so", "than", "too", "very", "just", "now",
    # Common words
    "when", "where", "why", "how", "what", "who", "which", "whose", "whom",
    # Numbers (common)
    "one", "two", "three", "first", "second", "third",
}


def get_stop_words() -> set[str]:
    """Get the set of English stop words.

    Returns:
        Set of stop words to filter during text analysis
    """
    return ENGLISH_STOP_WORDS.copy()

