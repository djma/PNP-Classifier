from model import *

nounClassifier = NounClassifier()
nounClassifier.loadClassData('../data/places-names.tsv', 'places')
nounClassifier.loadClassData('../data/people-names.tsv', 'people')
nounClassifier.loadClassData('../data/apps-names.tsv', 'apps')

while True:
  pnp = raw_input("Enter proper noun phrase to classify: ")
  print nounClassifier.classify(pnp)

