# SETUP
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
from sklearn.metrics import auc
import numpy as np
import json
import requests
import pandas as pd

# SYSTEM_TYPE = 'basic'
SYSTEM_TYPE = 'advanced'
QRELS_FILE = f'qrels1_{SYSTEM_TYPE}.txt'
QUERY_URL = 'http://localhost:8982/solr/reviews/select?fl=score%20*&fq=rating_score%3A%20%5B8.0%20TO%2010.0%5D&indent=true&q.op=OR&q=genre%3Ajazz%5E2%0Areview_content%3Acalm%0Areview_content%3Aquiet%0Areview_content%3Aambient%0Areview_content%3Arelaxing%0Areview_content%3A%22classical%20music%22%5E2%0A!review_content%3A%22violent%22&rows=25'

# Read qrels to extract relevant documents
relevant = list(map(lambda el: [int(el.strip())], open(QRELS_FILE).readlines()))
# Get query results from Solr instance
results = requests.get(QUERY_URL).json()['response']['docs']


# METRICS TABLE
# Define custom decorator to automatically calculate metric based on key
metrics = {}
metric = lambda f: metrics.setdefault(f.__name__, f)
print(metric)

@metric
def ap(results, relevant):
    """Average Precision"""
    for doc in results:
        print(doc['reviewid'])
    precision_values = [
        len([
            doc 
            for doc in results[:idx]
            if doc['reviewid'] in relevant
        ]) / idx 
        for idx in range(1, len(results))
    ]
    return sum(precision_values)/len(precision_values)

@metric
def p10(results, relevant, n=10):
    """Precision at N"""
    return len([doc for doc in results[:n] if doc['reviewid'] in relevant])/n

def calculate_metric(key, results, relevant):
    return metrics[key](results, relevant)

# Define metrics to be calculated
evaluation_metrics = {
    'ap': 'Average Precision',
    'p10': 'Precision at 10 (P@10)'
}

# Calculate all metrics and export results as LaTeX table
df = pd.DataFrame([['Metric','Value']] +
    [
        [evaluation_metrics[m], calculate_metric(m, results, relevant)]
        for m in evaluation_metrics
    ]
)

with open(f'results_{SYSTEM_TYPE}.tex','w') as tf:
    tf.write(df.to_latex())


# PRECISION-RECALL CURVE
# Calculate precision and recall values as we move down the ranked list
precision_values = [
    len([
        doc 
        for doc in results[:idx]
        if doc['reviewid'] in relevant
    ]) / idx 
    for idx, _ in enumerate(results, start=1)
]

recall_values = [
    len([
        doc for doc in results[:idx]
        if doc['reviewid'] in relevant
    ]) / len(relevant)
    for idx, _ in enumerate(results, start=1)
]

precision_recall_match = {k: v for k,v in zip(recall_values, precision_values)}

# Extend recall_values to include traditional steps for a better curve (0.1, 0.2 ...)
recall_values.extend([step for step in np.arange(0.1, 1.1, 0.1) if step not in recall_values])
recall_values = sorted(set(recall_values))

# Extend matching dict to include these new intermediate steps
for idx, step in enumerate(recall_values):
    if step not in precision_recall_match:
        if recall_values[idx-1] in precision_recall_match:
            precision_recall_match[step] = precision_recall_match[recall_values[idx-1]]
        else:
            precision_recall_match[step] = precision_recall_match[recall_values[idx+1]]

disp = PrecisionRecallDisplay([precision_recall_match.get(r) for r in recall_values], recall_values)

auc_precision_recall = auc(disp.recall,disp.precision)
print(f'Area Under Curve: {auc_precision_recall}')
disp.plot()
plt.savefig(f'precision_recall_{SYSTEM_TYPE}.pdf')
