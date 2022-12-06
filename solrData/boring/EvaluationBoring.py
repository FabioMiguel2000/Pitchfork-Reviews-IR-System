# SETUP
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import json
import requests
import pandas as pd





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

QRELS_FILE = "relevantBasicOrigD.txt"
QUERY_URL = 'http://localhost:8983/solr/reviews/select?q=boring&q.op=AND&defType=edismax&indent=true&rows=25&qf=review_content%5E1%20keywords%5E1'

# Read qrels to extract relevant documents
relevantBasicOrigD = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
resultsBasicOrigD = requests.get(QUERY_URL).json()['response']['docs']

QRELS_FILE = "relevantExtendedOrigD.txt"
QUERY_URL = 'http://localhost:8984/solr/reviews/select?q=boring&q.op=AND&defType=edismax&indent=true&rows=25&qf=review_content%5E2%20keywords%5E5&boost=sum(1,%20div(abs(sum(-10,%20score)),10))'

# Read qrels to extract relevant documents
relevantExOrigD = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
resultsExOrigD = requests.get(QUERY_URL).json()['response']['docs']

QRELS_FILE = "relevantExtendedOrigC.txt"
QUERY_URL = 'http://localhost:8986/solr/reviews/select?q=boring&q.op=AND&defType=edismax&indent=true&rows=25&qf=review_content%5E2%20keywords%5E5&boost=sum(1,%20div(abs(sum(-10,%20score)),10))'

# Read qrels to extract relevant documents
relevantExOrigC = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
resultsExOrigC = requests.get(QUERY_URL).json()['response']['docs']

QRELS_FILE = "relevantExtendedEmpty.txt"
QUERY_URL = 'http://localhost:8987/solr/reviews/select?q=boring&q.op=AND&defType=edismax&indent=true&rows=25&qf=review_content%5E2%20keywords%5E5&boost=sum(1,%20div(abs(sum(-10,%20score)),10))'

# Read qrels to extract relevant documents
relevantExEmpty = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
resultsExEmpty = requests.get(QUERY_URL).json()['response']['docs']

QRELS_FILE = "relevantExtendedClean.txt"
QUERY_URL = 'http://localhost:8988/solr/reviews/select?q=boring&q.op=AND&defType=edismax&indent=true&rows=25&qf=review_content%5E2%20keywords%5E5&boost=sum(1,%20div(abs(sum(-10,%20score)),10))'

# Read qrels to extract relevant documents
relevantExClean = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
resultsExClean = requests.get(QUERY_URL).json()['response']['docs']



calculate_metrics_all(resultsBasicOrigD, relevantBasicOrigD, 'resultsBasicOrigD.txt', True)
calculate_metrics_all(resultsExOrigD, relevantExOrigD, 'resultsExtendedOrigD.txt', False)
calculate_metrics_all(resultsExOrigC, relevantExOrigC, 'resultsExtendedOrigC.txt', False)
calculate_metrics_all(resultsExEmpty, relevantExEmpty, 'resultsExtendedEmpty.txt', False)
calculate_metrics_all(resultsExClean, relevantExClean, 'resultsExtendedClean.txt', False)

recall_valuesBasicOrigD, yBasicOrigD = precision_recall_curve(resultsBasicOrigD, relevantBasicOrigD, True)
recall_valuesExOrigD, yExOrigD = precision_recall_curve(resultsExOrigD, relevantExOrigD, False)
recall_valuesExOrigC, yExOrigC = precision_recall_curve(resultsExOrigC, relevantExOrigC, False)
recall_valuesExEmpty, yExEmpty = precision_recall_curve(resultsExEmpty, relevantExEmpty, False)
recall_valuesExClean, yExClean = precision_recall_curve(resultsExClean, relevantExClean, False)

plt.plot(recall_valuesBasicOrigD, yBasicOrigD, label="Basic schema, original content, no keywords")
plt.plot(recall_valuesExOrigD, yExOrigD, label="Extended schema, original content, no keywords")
plt.plot(recall_valuesExOrigC, yExOrigC, label="Extended schema, original content, with keywords")
plt.plot(recall_valuesExEmpty, yExEmpty, label="Extended schema, empty content, with keywords")
plt.plot(recall_valuesExClean, yExClean, label="Extended schema, clean content, with keywords")
#plt.plot(recall_values_With, yWith, label="With Schema", color = 'forestgreen')

plt.xlabel("Recall")
plt.ylabel("Precision")

plt.legend()

plt.savefig('BoringplotTogether.png')


