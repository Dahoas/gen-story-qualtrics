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
with open('carp_results.csv', 'w') as f:
	json.dump(results, f)