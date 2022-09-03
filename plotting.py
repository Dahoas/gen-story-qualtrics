


import numpy as np
import matplotlib.pyplot as plt
import json

# Cluster bars by topic
# Each subcluster is a model

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

carp_results['gedi'] = gedi_results
results = carp_results

# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8))

# set height of bar
CARP = [acc for key, acc in results['carp'].items()]
for label, key in zip(labels, results['carp'].keys()):
	print(label, key)
COOP = [acc for key, acc in results['coop'].items()]
NEOX = [acc for key, acc in results['neox'].items()]
GEDI = [acc for key, acc in results['gedi'].items()]

ALIGNMENT_CARP = CARP[:3]
TOPIC_CARP = CARP[3:]
ALIGNMENT_COOP = COOP[:3]
TOPIC_COOP = COOP[3:]
ALIGNMENT_NEOX = NEOX[:3]
TOPIC_NEOX = NEOX[3:]
ALIGNMENT_GEDI = GEDI[:3]
TOPIC_GEDI = GEDI[3:]

def avg(v):
	return sum(v)/len(v)


# Set position of bar on X axis
br1 = np.arange(len(ALIGNMENT_CARP))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]


# Make the plot
plt.bar(br1, ALIGNMENT_NEOX, color ='#000000', width = barWidth,
        edgecolor ='grey', label ='NeoX')
plt.bar(br2, ALIGNMENT_CARP, color ='#208ce1', width = barWidth,
        edgecolor ='grey', label ='Default CARP LM')
plt.bar(br3, ALIGNMENT_COOP, color ='#d25237', width = barWidth,
        edgecolor ='grey', label ='Alignment CARP LM')
plt.bar(br4, ALIGNMENT_GEDI, color ='#71c56c', width = barWidth,
        edgecolor ='grey', label ='Alignment GEDI')


# Adding Xticks
plt.xlabel('Alignment', fontweight ='bold', fontsize = 15)
plt.ylabel('Selected Human Preference (%)', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(ALIGNMENT_CARP))],
        alignments)

order = [1,2,0,3]
legend_names = ['Default CARP LM', ]
plt.legend()
plt.show()
plt.savefig('alignment.png')

plt.clf()

#TOPIC CARP
# Set position of bar on X axis
br1 = np.arange(len(TOPIC_CARP))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]

# Make the plot
plt.bar(br1, TOPIC_NEOX, color ='#000000', width = barWidth,
        edgecolor ='grey', label ='NeoX')
plt.bar(br2, TOPIC_CARP, color ='#208ce1', width = barWidth,
        edgecolor ='grey', label ='Default CARP LM')

plt.bar(br3, TOPIC_COOP, color ='#d25237', width = barWidth,
        edgecolor ='grey', label ='Pseudo CARP LM')
plt.bar(br3, ALIGNMENT_GEDI, color ='#71c56c', width = barWidth,
        edgecolor ='grey', label ='Alignment GEDI')


# Adding Xticks
plt.xlabel('Critique', fontweight ='bold', fontsize = 15)
plt.ylabel('Selected Human Preference (%)', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(TOPIC_CARP))],
        topics[:8])

plt.legend()
plt.show()
plt.savefig('topics.png')