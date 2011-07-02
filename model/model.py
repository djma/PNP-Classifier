

def loadCharNGram(ngramCount, pnp, n):
  # Prepend n-1 whitespaces and eol unique character (^) 
  pnp = (n-1)*' ' + pnp + '^'
  ngramCount[ngram] = ngramCount.setdefault(ngram, 0) + 1



class NounClassifier:
  # A dict of dict: classname -> ngram -> count
  # character n-gram
  _cng = dict()
  N_FOR_CNG = 6
  # word-length ngram
  _wlng = dict()
  N_FOR_WLNG = 4

  def __init__(self):
    
  def loadClassData(self, filename, classname):
    if classname not in _cng:
      _cng[classname] = dict()
      _wlng[classname] = dict()
    f = open(filename)
    for pnp in f:
      pnp = pnp.strip()
      for n in range(1, N_FOR_CNG+1):
        loadCharNGram(self._cng[classname], pnp, n)
      for n in range(1, N_FOR_WLNG+1):
        loadWordLengthNGram(self._wlng[classname], pnp, n)
