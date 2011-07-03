from random import random, seed
from model import *

# FOR filtering out non-utf 8 stuff.. just ugly, preliminary                                                          
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

seed(42)

places = open('../data/places-names.tsv')
people = open('../data/people-names.tsv')
apps = open('../data/apps-names.tsv')

places_test = open('../data/places-test.tsv', 'w')
people_test = open('../data/people-test.tsv', 'w')
apps_test = open('../data/apps-test.tsv', 'w')

places_train = open('../data/places-train.tsv', 'w')
people_train = open('../data/people-train.tsv', 'w')
apps_train = open('../data/apps-train.tsv', 'w')

for line in places:
  if not is_ascii(line):
    continue
  if random() < 0.1:
    places_test.write(line)
  else:
    places_train.write(line)

for line in people:
  if not is_ascii(line):
    continue
  if random() < 0.1:
    people_test.write(line)
  else:
    people_train.write(line)

for line in apps:
  if not is_ascii(line):
    continue
  if random() < 0.1:
    apps_test.write(line)
  else:
    apps_train.write(line)


places_test.close()
people_test.close()
apps_test.close()
places_train.close()
people_train.close()
apps_train.close()

places_test = open('../data/places-test.tsv')
people_test = open('../data/people-test.tsv')
apps_test = open('../data/apps-test.tsv')

nounClassifier = NounClassifier()
nounClassifier.loadClassData('../data/places-train.tsv', 'places')
nounClassifier.loadClassData('../data/people-train.tsv', 'people')
nounClassifier.loadClassData('../data/apps-train.tsv', 'apps')

total = 0
success = 0
for line in places_test:
  if nounClassifier.classify(line) == 'places':
    total += 1
    success += 1
  else:
    total += 1
for line in people_test:
  if nounClassifier.classify(line) == 'people':
    total += 1
    success += 1
  else:
    total += 1
for line in apps_test:
  if nounClassifier.classify(line) == 'apps':
    total += 1
    success += 1
  else:
    total += 1

print float(success)/float(total)

