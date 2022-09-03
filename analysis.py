import numpy as np
import matplotlib.pyplot as plt
import json


labels = ['good', 'neutral', 'evil',
		  'family', 'music', 'accident',
		  'religion', 'imagery', 'fighting',
		  'romance', 'horror']
alignments = ['good', 'neutral', 'evil']
topics = ['family', 'music', 'accident',
		  'religion', 'imagery', 'fighting',
		  'romance', 'horror', 'own response']

with open('carp_results.csv', 'r') as f:
    carp_results = json.load(f)
with open('gedi_results.csv', 'r') as f:
    gedi_results = json.load(f)
with open('processed_carp_data.csv', 'r') as f:
    carp_data = json.load(f)
with open('processed_gedi_data.csv', 'r') as f:
    gedi_data = json.load(f)
with open('carp_agreements.json', 'r') as f:
    carp_agreements = json.load(f)
with open('gedi_agreements.json', 'r') as f:
    gedi_agreements = json.load(f)

carp_results['gedi'] = gedi_results
results = carp_results
carp_data['gedi'] = gedi_data
data = carp_data
carp_agreements['gedi'] = gedi_agreements
agreements = carp_agreements

cnt = 0
cum = 0
for model in agreements:
    if model != '':
        for label in agreements[model]:
            cum += sum(agreements[model][label])
            cnt += len(agreements[model][label])
print('global_agreemen', cum / cnt)

sliced_agreements = {}
for model in agreements:
    cnt = 0
    cum = 0
    for label in agreements[model]:
        cum += sum(agreements[model][label])
        cnt += len(agreements[model][label])
    agreement = cum / cnt
    sliced_agreements[model] = agreement

for label in agreements['gedi']:
    cnt = 0
    cum = 0
    for model in agreements:
        if label in agreements[model]:
            cum += sum(agreements[model][label])
            cnt += len(agreements[model][label])
    agreement = cum / cnt
    sliced_agreements[label] = agreement

print(json.dumps(sliced_agreements, indent=4))
