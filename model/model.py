from math import log


#Model Parameters
N_FOR_CNG = 6
N_FOR_WLNG = 4


def loadCharNGram(ngramCount, pnp, n):
  pnpLength = len(pnp)
  # Prepend n-1 whitespaces and eol unique character (^) 
  pnp = (n-1)*' ' + pnp + '^'
  for i in range(pnpLength):
    ngram = pnp[i:i+n]
    ngramCount[ngram] = ngramCount.setdefault(ngram, 0) + 1


def loadWordLengthNGram(ngramCount, pnp, n):
  pnp = tuple((n-1)*[0] + map(len, pnp.split()) + [0])
  wlngLength = len(pnp) - n
  ngramCount[tuple((n-1)*[0])] = ngramCount.setdefault(tuple((n-1)*[0]), 0) + 1
  for i in range(wlngLength):
    ngram = pnp[i:i+n]
    ngramCount[ngram] = ngramCount.setdefault(ngram, 0) + 1



def getEmpiricalCondProb(ngramCount, ngram):
  if ngram in ngramCount:
    return float(ngramCount[ngram]) / float(ngramCount[ngram[0:-1]])
  else:
    return 0


def getSmoothedCondProb(ngramCount, ngram):
  if len(ngram) == 0:
    return 1
  else:
    lmbda = conditioningContext(ngram)
    return ( lmbda * getEmpiricalCondProb(ngramCount, ngram) +
             (1-lmbda) * getSmoothedCondProb(ngramCount, ngram[1:])
           )


def getLogWordProb(ngramCount, word, n):
  # The variable 'word' should already be padded accordingly
  logCumProb = 0.0
  for i in range(len(word)-n):
    ngram = word[i:i+n]
    logCumProb += log(getSmoothedCondProb(ngramCount, ngram))
  return logCumProb




def conditioningContext(ngram):
  return 0.7

class NounClassifier:
  def __init__(self):
    # A dict of dict: classname -> ngram -> count
    # character n-gram
    self._cng = dict()
    # word-length ngram
    self._wlng = dict()
    return

  def loadClassData(self, filename, classname):
    if classname not in self._cng:
      self._cng[classname] = dict()
      self._wlng[classname] = dict()
    f = open(filename)
    for pnp in f:
      # Should we filter non utf8 chars for now?
      # TODO

      pnp = pnp.strip().lower()
      for n in range(0, N_FOR_CNG+1):
        loadCharNGram(self._cng[classname], pnp, n)
      for n in range(0, N_FOR_WLNG+1):
        loadWordLengthNGram(self._wlng[classname], pnp, n)

  def getLogWLNGProb(self, pnp, classname):
    if classname not in self._wlng:
      print "Model has not been trained for class: " + classname
    wordLengths = tuple((N_FOR_WLNG-1)*[0] + map(len, pnp.split()) + [0])
    return getLogWordProb(self._wlng[classname], wordLengths, N_FOR_WLNG)
    

  def classify(self, pnp):
    return
