def evaluate(relevant_docs, retrieved_docs):
    relevant = set(relevant_docs)
    retrieved = set(retrieved_docs)
    true_positives = len(relevant.intersection(retrieved))
    precision = true_positives / len(retrieved) if len(retrieved) > 0 else 0
    recall = true_positives / len(relevant) if len(relevant) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision,recall,f1