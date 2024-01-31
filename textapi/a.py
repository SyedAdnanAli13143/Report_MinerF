import pandas as pd
import re


data_text = """
S.No             Item & Description                                                           Qty             Rate
1                 advanced shooting capabilities                         1         $899.00
                   that is nice.
2                Fitness Tracker Activity tracker with heart rate monitoring                    1         $129.00

3                Laptop Lightweight laptop with a powerful processor                            1       $1,199.00
"""


lines = [line.strip() for line in data_text.strip().split('\n')]
lines = [line for line in lines if line]


columns = re.split(r'\s{2,}', lines[0].strip())


data = []
current_entry = {col: [] for col in columns}

for line in lines[1:]:
    values = re.split(r'\s{2,}', line.strip())
    
 
    if re.match(r'^\d', line):
        if current_entry:
            data.append(current_entry)
            current_entry = {col: [] for col in columns}
    
 
    for col, val in zip(columns, values):
        current_entry[col].append(val)


def find_best_match(multiline, previous_entries):
    best_match = None
    max_similarity = 0
    for entry in previous_entries:
        entry_values = entry if isinstance(entry, list) else [entry]
        for entry_value in entry_values:
            similarity = len(set(multiline.lower().split()) & set(entry_value.lower().split()))
            if similarity > max_similarity:
                max_similarity = similarity
                best_match = entry_value
    return best_match


if current_entry:
    data.append(current_entry)


for entry in data:
    for col in columns:
        if len(entry[col]) > 1:
            entry[col] = find_best_match(entry[col][0], [e[col] for e in data if e != entry])

df = pd.DataFrame(data, columns=columns)


for column in df.columns:
    print(f"{column}: {df[column].tolist()}")
