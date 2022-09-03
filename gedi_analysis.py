from numpy import NaN
import numpy as np
import pandas as pd
import json



df = pd.read_csv("gedi_data.csv")
df = df.drop(labels=[0,1], axis=0)

with open("scratch1.txt",'w') as f:
	for column in df.columns:
		f.write(str(column)+'\n')

#QID8 - QID37 are alignment
#QID101 - QID182 are content
#Q312 and larger are qualitative
#_TEXT questions can be discarded

alignments = ['good', 'neutral', 'evil']
topics = ['family', 'music', 'accident', 'religion', 'imagery', 'fighting', 'romantic', 'horror', 'other']  # Ordered according to option order in survey
labels = ['evil', 'neutral', 'good', 'accident', 'family', 'fighting', 'horror', 'imagery', 'music', 'religion', 'romantic']  # Ordered according to ordering of topics in survey questions
num_to_label = [num + 1 if num < 3 else num - 2 for num, label in enumerate(labels)]
assert len(labels) == 11

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
	return int(num)

filtered_df = []
col_labels = []
cnt = 0
for col in df.columns:
	if "TEXT" in col or 'QID' not in col:
		continue
	num = get_num(col)
	# Ignore _TEXT columns
	if (8 <= num and num <= 37) or (num >= 101 and num <= 182):
		filtered_df.append(col)
		col_labels.append(labels[cnt // 10])  # Questions appear in group of 10 on survey
		cnt += 1
assert len(filtered_df) == 110  # 11 labels, 10 samples each

data = {label:
			[]
		for label in labels}

num_to_label = {
	'alignment': {1: 'good', 2: 'neutral', 3: 'evil'},
	'topic': {(ind+1): topic for ind, topic in enumerate(topics)}
}

print(num_to_label)

for qualtrics_col, label in zip(filtered_df, col_labels):
	for entry in df[qualtrics_col]:
		if not np.isnan(float(entry)):
			entry = int(entry)
			if label in topics:
				topic_entry = num_to_label['topic'][entry]
			elif label in alignments:
				topic_entry = num_to_label['alignment'][entry]
			else:
				print(label)
				raise NotImplemented
			data[label].append(topic_entry)

#print(json.dumps(data, indent=4, sort_keys=True))

results = {label:
				0.0
			for label in labels}

for label in data:
	entries = data[label]
	num_entries = len(entries)
	cnt = sum([entry == label for entry in entries])
	if num_entries == 0:
		acc = 0.0
	else:
		acc = cnt/num_entries
	results[label] = acc

print(json.dumps(results, indent=4, sort_keys=True))
with open('gedi_results.csv', 'w') as f:
	json.dump(results, f)