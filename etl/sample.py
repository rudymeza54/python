

import csv


with open('sample.csv','r') as csv_file:

    reader = csv.reader(csv_file, delimiter = ',')


    for row in reader:
        print(row)