# The CSV file with the relation comes from the official STIX documentation with a few additions
# However, some entries might represent multiple entries and therefore we want to explicit them

# [EXAMPLE] attack-pattern,uses,"malware,tool",using
#   [-] attack-pattern,uses,malware,using
#   [-] attack-pattern,uses,tool,using

import csv
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# Saving rows
file = open("./Relation-Extraction/SROs.csv")
csvreader = csv.reader(file)
header = next(csvreader)
rows = []
for row in csvreader:
    rows.append(row)
file.close()

with open('./Relation-Extraction/Relations.csv', 'w') as f:
    writer = csv.writer(f, lineterminator = '\n')
    writer.writerow(header)
    for row in rows:
        new_row = row
        hasComma = False
        for i in range(4):
            if ',' in row[i]:
                hasComma = True
                split = row[i].split(',')
                for item in split:
                    new_row[i] = item

                    writer.writerow(new_row)
        if not hasComma:
            new_row[1] = lemmatizer.lemmatize(new_row[1], pos='v')
            writer.writerow(new_row)