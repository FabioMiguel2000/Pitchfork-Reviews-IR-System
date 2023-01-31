import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import json
import requests
import pandas as pd
from sklearn.metrics import auc

# METRICS TABLE
# Define custom decorator to automatically calculate metric based on key
metrics = {}
metric = lambda f: metrics.setdefault(f.__name__, f)

@metric
def ap(results, relevant, basic):
    """Average Precision"""
    if not basic:
        precision_values = [
            len([
                doc 
                for doc in results[:idx]
                if str(doc['reviewid']) in relevant
            ]) / idx 
            for idx in range(1, len(results))
        ]
    else:
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
def p10(results, relevant, basic, n=10):
    """Precision at N"""
    if not basic:
        return len([doc for doc in results[:n] if str(doc['reviewid']) in relevant])/n
    return len([doc for doc in results[:n] if str(doc['reviewid'][0]) in relevant])/n

@metric
def p20(results, relevant, basic, n=20):
    """Precision at N"""
    if not basic:
        return len([doc for doc in results[:n] if str(doc['reviewid']) in relevant])/n
    return len([doc for doc in results[:n] if str(doc['reviewid'][0]) in relevant])/n

@metric
def p05(results, relevant,basic,  n=5):
    """Precision at N"""
    if not basic:
        return len([doc for doc in results[:n] if str(doc['reviewid']) in relevant])/n
    return len([doc for doc in results[:n] if str(doc['reviewid'][0]) in relevant])/n

@metric
def p25(results, relevant, basic, n=25):
    """Precision at N"""
    if not basic:
        return len([doc for doc in results[:n] if str(doc['reviewid']) in relevant])/n
    return len([doc for doc in results[:n] if str(doc['reviewid'][0]) in relevant])/n

@metric
def p15(results, relevant, basic, n=15):
    """Precision at N"""
    if not basic:
        return len([doc for doc in results[:n] if str(doc['reviewid']) in relevant])/n
    return len([doc for doc in results[:n] if str(doc['reviewid'][0]) in relevant])/n

@metric
def recall(results, relevant, basic):
    """Precision at N"""
    if not basic:
        return len([doc for doc in results if str(doc['reviewid']) in relevant])/len(relevant)
    return len([doc for doc in results if str(doc['reviewid'][0]) in relevant])/len(relevant)

def calculate_metric(key, results, relevant, basic):
    return metrics[key](results, relevant, basic)

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
def calculate_metrics_all(results, relevant, name, basic):
    df = pd.DataFrame([['Metric','Value']] +
        [
            [evaluation_metrics[m], calculate_metric(m, results, relevant, basic)]
            for m in evaluation_metrics
        ]
    )

    with open(name,'w') as tf: #results.tex
        tf.write(df.to_latex())

# PRECISION-RECALL CURVE
# Calculate precision and recall values as we move down the ranked list
def precision_recall_curve(results, relevant, basic):
    if not basic:
        precision_values = [
            len([
                doc 
                for doc in results[:idx]
                if str(doc['reviewid']) in relevant
            ]) / idx 
            for idx, _ in enumerate(results, start=1)
        ]

        recall_values = [
            len([
                doc for doc in results[:idx]
                if str(doc['reviewid']) in relevant
            ]) / len(relevant)
            for idx, _ in enumerate(results, start=1)
        ]
    else:
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

    auc_precision_recall = auc(recall_values, precision_values)
    print(f'Area Under Curve: {auc_precision_recall}')
    # Extend recall_values to include traditional steps for a bett
    # er curve (0.1, 0.2 ...)
    recall_values.extend([step for step in np.arange(0.1, 1.1, 0.001) if step not in recall_values])
    recall_values = sorted(set(recall_values))
    # Extend matching dict to include these new intermediate steps
    for idx, step in enumerate(recall_values):
        if step not in precision_recall_match:
            if recall_values[idx-1] in precision_recall_match:
                precision_recall_match[step] = precision_recall_match[recall_values[idx-1]]
            else:
                precision_recall_match[step] = precision_recall_match[recall_values[idx+1]]

    y = [precision_recall_match.get(r) for r in recall_values]
    return recall_values, y

# Information need:  I want to find reviews about albums that include jazz and piano
# QUERY: (dismax used:)
# q: ("jazz piano"~20)^2 piano jazz
# defType: dismax
# keywords review_content genre^3

# sytem 1, 2, 3 have similar results
# system 4 and 5 have very different results compared to the ones in 1, 2, 3
#


# SYSTEM_1
QRELS_FILE = "./qrels/system_1.txt"
QUERY_URL = 'http://localhost:8981/solr/reviews/select?defType=dismax&fl=score%20*&indent=true&q.op=OR&q=(%22jazz%20piano%22~20)%5E2%20piano%20jazz&qf=keywords%20review_content%20genre%5E5&rows=25'

# Read qrels to extract relevant documents
relevant_1 = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
results_1 = requests.get(QUERY_URL).json()['response']['docs']

# SYSTEM_2
QRELS_FILE = "./qrels/system_2.txt"
QUERY_URL = 'http://localhost:8982/solr/reviews/select?defType=dismax&fl=score%20*&indent=true&q.op=OR&q=(%22jazz%20piano%22~20)%5E2%20piano%20jazz&qf=keywords%20review_content%20genre%5E5&rows=25'

# Read qrels to extract relevant documents
relevant_2 = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
results_2 = requests.get(QUERY_URL).json()['response']['docs']

# SYSTEM_3
QRELS_FILE = "./qrels/system_3.txt"
QUERY_URL = 'http://localhost:8983/solr/reviews/select?defType=dismax&fl=score%20*&indent=true&q.op=OR&q=(%22jazz%20piano%22~20)%5E2%20piano%20jazz&qf=keywords%20review_content%20genre%5E5&rows=25'

# Read qrels to extract relevant documents
relevant_3 = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
results_3 = requests.get(QUERY_URL).json()['response']['docs']

# SYSTEM_4
QRELS_FILE = "./qrels/system_4.txt"
QUERY_URL = 'http://localhost:8984/solr/reviews/select?defType=dismax&fl=score%20*&indent=true&q.op=OR&q=(%22jazz%20piano%22~20)%5E2%20piano%20jazz&qf=keywords%20review_content%20genre%5E5&rows=25'

# Read qrels to extract relevant documents
relevant_4 = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
results_4 = requests.get(QUERY_URL).json()['response']['docs']

# SYSTEM_5
QRELS_FILE = "./qrels/system_5.txt"
QUERY_URL = 'http://localhost:8985/solr/reviews/select?defType=dismax&fl=score%20*&indent=true&q.op=OR&q=(%22jazz%20piano%22~20)%5E2%20piano%20jazz&qf=keywords%20review_content%20genre%5E5&rows=25'

# Read qrels to extract relevant documents
relevant_5 = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
results_5 = requests.get(QUERY_URL).json()['response']['docs']

# SYSTEM_6
QRELS_FILE = "./qrels/system_6.txt"
QUERY_URL = 'http://localhost:8986/solr/reviews/select?defType=dismax&fl=score%20*&indent=true&q.op=OR&q=(%22jazz%20piano%22~20)%5E2%20piano%20jazz&qf=keywords%20review_content%20genre%5E5&rows=25'

# Read qrels to extract relevant documents
relevant_6 = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
results_6 = requests.get(QUERY_URL).json()['response']['docs']


calculate_metrics_all(results_1, relevant_1, './results/results_system_1.txt', True)
calculate_metrics_all(results_2, relevant_2, './results/results_system_2.txt', False)
calculate_metrics_all(results_3, relevant_3, './results/results_system_3.txt', False)
calculate_metrics_all(results_4, relevant_4, './results/results_system_4.txt', False)
calculate_metrics_all(results_5, relevant_5, './results/results_system_5.txt', False)
calculate_metrics_all(results_6, relevant_6, './results/results_system_6.txt', False)


recall_values_1, y_1 = precision_recall_curve(results_1, relevant_1, True)
recall_values_2, y_2 = precision_recall_curve(results_2, relevant_2, False)
recall_values_3, y_3 = precision_recall_curve(results_3, relevant_3, False)
recall_values_4, y_4 = precision_recall_curve(results_4, relevant_4, False)
recall_values_5, y_5 = precision_recall_curve(results_5, relevant_5, False)
recall_values_6, y_6 = precision_recall_curve(results_6, relevant_6, False)


plt.plot(recall_values_1, y_1, label="System 1")
plt.plot(recall_values_2, y_2, label="System 2")
plt.plot(recall_values_3, y_3, label="System 3")
plt.plot(recall_values_4, y_4, label="System 4")
plt.plot(recall_values_5, y_5, label="System 5")
plt.plot(recall_values_6, y_6, label="System 6")

#plt.plot(recall_values_With, yWith, label="With Schema", color = 'forestgreen')

plt.xlabel("Recall")
plt.ylabel("Precision")

plt.legend()

plt.savefig('./plots/StudyingPlotTogether.png')


