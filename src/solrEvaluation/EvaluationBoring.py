# SETUP
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import json
import requests
import pandas as pd

QRELS_FILE = "withSchema.txt"
QUERY_URL = 'http://localhost:8984/solr/reviews/select?q=review_content:boring%5E5%0A-title:boring%0A-review_content:"doesn\'t%20boring"~5%0A-review_content:"not%20boring"~5%0A-review_content:"never%20boring"~5%0Areview_content:"is%20boring"~5%0A-review_content:"%20"(%5C")"%20boring%20"(%5C")"%20"~3%5E2&q.op=OR&rows=25&wt=json'

# Read qrels to extract relevant documents
relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
results = requests.get(QUERY_URL).json()['response']['docs']

print(len(results))


# METRICS TABLE
# Define custom decorator to automatically calculate metric based on key
metrics = {}
metric = lambda f: metrics.setdefault(f.__name__, f)

@metric
def ap(results, relevant):
    """Average Precision"""
    precision_values = [
        len([
            doc 
            for doc in results[:idx]
            if str(doc['reviewid'][0]) in relevant
        ]) / idx 
        for idx in range(1, len(results))
    ]
    return sum(precision_values)/len(precision_values)


@metric
def p10(results, relevant, n=10):
    """Precision at N"""
    return len([doc for doc in results[:n] if str(doc['reviewid'][0]) in relevant])/n

@metric
def p20(results, relevant, n=20):
    """Precision at N"""
    return len([doc for doc in results[:n] if str(doc['reviewid'][0]) in relevant])/n

@metric
def p05(results, relevant, n=5):
    """Precision at N"""
    return len([doc for doc in results[:n] if str(doc['reviewid'][0]) in relevant])/n

@metric
def p25(results, relevant, n=25):
    """Precision at N"""
    return len([doc for doc in results[:n] if str(doc['reviewid'][0]) in relevant])/n

@metric
def p15(results, relevant, n=15):
    """Precision at N"""
    return len([doc for doc in results[:n] if str(doc['reviewid'][0]) in relevant])/n

@metric
def recall(results, relevant):
    """Precision at N"""
    return len([doc for doc in results if str(doc['reviewid'][0]) in relevant])/len(relevant)

def calculate_metric(key, results, relevant):
    return metrics[key](results, relevant)

# Define metrics to be calculated
evaluation_metrics = {
    'ap': 'Average Precision',
    'p05': 'Precision at 5 (P@05)',
    'p10': 'Precision at 10 (P@10)',
    'p15': 'Precision at 15 (P@15)',
    'p20': 'Precision at 20 (P@20)',
    'p25': 'Precision at 25 (P@25)', 
    'recall': 'Recall'
}

# Calculate all metrics and export results as LaTeX table
df = pd.DataFrame([['Metric','Value']] +
    [
        [evaluation_metrics[m], calculate_metric(m, results, relevant)]
        for m in evaluation_metrics
    ]
)

with open('results.tex','w') as tf:
    tf.write(df.to_latex())

# PRECISION-RECALL CURVE
# Calculate precision and recall values as we move down the ranked list
precision_values = [
    len([
        doc 
        for doc in results[:idx]
        if str(doc['reviewid'][0]) in relevant
    ]) / idx 
    for idx, _ in enumerate(results, start=1)
]

recall_values = [
    len([
        doc for doc in results[:idx]
        if str(doc['reviewid'][0]) in relevant
    ]) / len(relevant)
    for idx, _ in enumerate(results, start=1)
]
precision_recall_match = {k: v for k,v in zip(recall_values, precision_values)}

# Extend recall_values to include traditional steps for a bett
# er curve (0.1, 0.2 ...)
recall_values.extend([step for step in np.arange(0.1, 1.1, 0.01) if step not in recall_values])
recall_values = sorted(set(recall_values))
# Extend matching dict to include these new intermediate steps
for idx, step in enumerate(recall_values):
    if step not in precision_recall_match:
        if recall_values[idx-1] in precision_recall_match:
            precision_recall_match[step] = precision_recall_match[recall_values[idx-1]]
        else:
            precision_recall_match[step] = precision_recall_match[recall_values[idx+1]]


disp = PrecisionRecallDisplay([precision_recall_match.get(r) for r in recall_values], recall_values)
disp.plot()
plt.savefig('precision_recall.png')


