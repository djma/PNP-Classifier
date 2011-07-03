from math import log

#Model Parameters
N_FOR_CNG = 6
N_FOR_WLNG = 4
WORD_LENGTH_NORMALIZATION_CONSTANT = 2.5


def normalizeString(pnp):
  pnp = pnp.strip().lower()
  pnp = ' '.join(pnp.split())
  return pnp

def loadCharNGram(ngramCount, pnp, n):
  pnpLength = len(pnp) + 1
  # Prepend n whitespaces and eol unique character (^) 
  pnp = n*' ' + pnp + '^'
  for i in range(pnpLength):
    ngram = pnp[i:i+n]
    ngramCount[ngram] = ngramCount.setdefault(ngram, 0) + 1


def loadWordLengthNGram(ngramCount, pnp, n):
  pnp = tuple(n*[0] + map(len, pnp.split()) + [0])
  wlngLength = len(pnp) - n + 1
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
      pnp = normalizeString(pnp)
      for n in range(0, N_FOR_CNG+1):
        loadCharNGram(self._cng[classname], pnp, n)
      for n in range(0, N_FOR_WLNG+1):
        loadWordLengthNGram(self._wlng[classname], pnp, n)

  def getLogWLNGProb(self, pnp, classname):
    if classname not in self._wlng:
      print "Model has not been trained for class: " + classname
    wordLengths = tuple((N_FOR_WLNG-1)*[0] + map(len, pnp.split()) + [0])
    return getLogWordProb(self._wlng[classname], wordLengths, N_FOR_WLNG)
    
  def getLogCNGProb(self, pnp, classname):
    # Conditional on the length of the word
    # Normalized by k/len where k is the word-length normalization constant
    logCumProb = 0.0
    pnpPadded = (N_FOR_CNG-1)*' ' + pnp + '^'
    idx = N_FOR_CNG-1
    while True:
      nextidx = pnpPadded.find(' ', idx)
      wordPadded = pnpPadded[idx-N_FOR_CNG+1:nextidx]
      wordLength = len(wordPadded) - N_FOR_CNG + 1
      logCumProb += (getLogWordProb(self._cng[classname], wordPadded, N_FOR_CNG) -\
                      getSmoothedCondProb(self._wlng, tuple([wordLength])))\
                    * WORD_LENGTH_NORMALIZATION_CONSTANT / wordLength
      idx = nextidx+1
      if nextidx == -1:
        break;
    return logCumProb

  def classify(self, pnp):
    pnp = normalizeString(pnp)
    mostLikelyClass = ''
    logLikOfBestClass = float("-inf")
    for classname in self._cng:
      logLikOfClass = self.getLogWLNGProb(pnp, classname) + \
                      self.getLogCNGProb(pnp, classname)
      if logLikOfBestClass < logLikOfClass:
        mostLikelyClass = classname
        logLikOfBestClass = logLikOfClass
    return mostLikelyClass
