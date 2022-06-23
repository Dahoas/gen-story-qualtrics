from numpy import NaN
import numpy as np
import pandas as pd
import json

df = pd.read_csv("my_data.csv")
df = df.drop(labels=25, axis=0)
#print(df)
with open("scratch.txt",'w') as f:
	for column in df.columns:
		f.write(str(column)+'\n')

#QID8 - QID99 are alignment
#QID100 - QID311 are content
#Q312 and larger are qualitative
#_TEXT questions can be discarded

models = ['coop', 'carp', 'neox']
labels = ['good', 'neutral', 'evil',
		  'family', 'music', 'accident',
		  'religion', 'imagery', 'fighting',
		  'romance', 'horror']
alignments = ['good', 'neutral', 'evil']
topics = ['family', 'music', 'accident',
		  'religion', 'imagery', 'fighting',
		  'romance', 'horror', 'own response']

def get_num(name):
	start = -1
	end = len(name)
	for ind, char in enumerate(name):
		#print(ind, char)
		if start < 0 and char.isnumeric():
			start = ind
		if start >= 0 and not char.isnumeric():
			end = ind
			break
	num = name[start:end]
	#print(num)
	return int(num)

filtered_df = []
for col in df.columns:
	num = get_num(col)
	# Ignore _TEXT columns
	if "TEXT" in col:
		continue
	if (8 <= num and num < 100) or (num > 101 and num <= 311):
		filtered_df.append(col)

# 92 total alignment questions


data = {model:
			{label:
				[]
			for label in labels}
		for model in models}
line_data = []
with open('examples.jsonl','r') as f:
	for line in f:
		question = json.loads(line)
		line_data.append(question)

assert(len(filtered_df) == len(line_data))

num_to_label = {
	'alignment': {1: 'good', 2: 'neutral', 3: 'evil'},
	'topic': {(ind+1): topic for ind, topic in enumerate(topics)}
}

for qualtrics_col, json_q in zip(filtered_df, line_data):
	label = json_q['label']
	model = json_q['model']
	for entry in df[qualtrics_col]:
		#print(float(entry))
		if not np.isnan(float(entry)):
			entry = int(entry)
			if label in topics:
				topic_entry = num_to_label['topic'][entry]
			elif label in alignments:
				topic_entry = num_to_label['alignment'][entry]
			else:
				raise NotImplemented
			data[model][label].append(topic_entry)

print(json.dumps(data, indent=4, sort_keys=True))

results = {model:
			{label:
				0.0
			for label in labels}
		for model in models}

for model in data:
	for label in data[model]:
		entries = data[model][label]
		num_entries = len(entries)
		cnt = sum([entry == label for entry in entries])
		if num_entries == 0:
			acc = 0.0
		else:
			acc = cnt/num_entries
		results[model][label] = acc

print(json.dumps(results, indent=4, sort_keys=True))


print(data['coop']['horror'])

import numpy as np
import matplotlib.pyplot as plt

# Cluster bars by topic
# Each subcluster is a model

# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8))

# set height of bar
CARP = [acc for key, acc in results['carp'].items()]
for label, key in zip(labels, results['carp'].keys()):
	print(label, key)
COOP = [acc for key, acc in results['coop'].items()]
NEOX = [acc for key, acc in results['neox'].items()]

ALIGNMENT_CARP = CARP[:3]
TOPIC_CARP = CARP[3:]
ALIGNMENT_COOP = COOP[:3]
TOPIC_COOP = COOP[3:]
ALIGNMENT_NEOX = NEOX[:3]
TOPIC_NEOX = NEOX[3:]

def avg(v):
	return sum(v)/len(v)

print(avg(ALIGNMENT_CARP))
print(avg(TOPIC_CARP))
print(avg(ALIGNMENT_COOP))
print(avg(TOPIC_COOP[:-2]))
print(avg(ALIGNMENT_NEOX))
print(avg(TOPIC_NEOX))

'''
# Set position of bar on X axis
br1 = np.arange(len(ALIGNMENT_CARP))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

# Make the plot
plt.bar(br1, ALIGNMENT_NEOX, color ='#000000', width = barWidth,
        edgecolor ='grey', label ='NeoX')
plt.bar(br2, ALIGNMENT_CARP, color ='#208ce1', width = barWidth,
        edgecolor ='grey', label ='Default CARP LM')
plt.bar(br3, ALIGNMENT_COOP, color ='#d25237', width = barWidth,
        edgecolor ='grey', label ='Alignment CARP LM')


# Adding Xticks
plt.xlabel('Alignment', fontweight ='bold', fontsize = 15)
plt.ylabel('Selected Human Preference (%)', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(ALIGNMENT_CARP))],
        alignments)

order = [1,2,0]
legend_names = ['Default CARP LM', ]
plt.legend()
plt.show()

plt.clf()

#TOPIC CARP
# Set position of bar on X axis
br1 = np.arange(len(TOPIC_CARP))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

# Make the plot
plt.bar(br1, TOPIC_NEOX, color ='#000000', width = barWidth,
        edgecolor ='grey', label ='NeoX')
plt.bar(br2, TOPIC_CARP, color ='#208ce1', width = barWidth,
        edgecolor ='grey', label ='Default CARP LM')

plt.bar(br3, TOPIC_COOP, color ='#d25237', width = barWidth,
        edgecolor ='grey', label ='Pseudo CARP LM')


# Adding Xticks
plt.xlabel('Critique', fontweight ='bold', fontsize = 15)
plt.ylabel('Selected Human Preference (%)', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(TOPIC_CARP))],
        topics[:8])

plt.legend()
plt.show()
'''