import data
import errors

class Damage():

  def __init__(self, *elements_):

    self._element = dict.fromkeys(data.getSupportedElementTypes(), 0.)

    for (type, damage) in elements_:
      if type not in data.getSupportedElementTypes():
        raise errors.InvalidElementError
      self._element[type] = damage

    pass

  def __setitem__(self, key, value):
    self._element[key] = value

  def __getitem__(self, key):
    return self._element[key]

  def __iadd__(self, other):
    for key in other._element.keys():
      self[key] += other[key]
      #self.__setitem__(key, self.__getitem__(key) + other.__getitem__(key))
    return self

  def __add__(self, other):
    total = Damage()
    for key in other._element.keys():
      total[key] = self[key] + other[key]
    return total

  def __str__(self):
    info = ''
    for key in self._element.keys():
      info += ('{}: {}, '.format(key, self._element[key]))
    return info[:-2] # remove last comma and space

  def total(self):
    d = 0
    for key in self._element.keys():
      d += self[key]
    return d

  def multiplyEachElementSeperately(self, factor_):
    for element, m in factor_.items():
      if element not in data.getSupportedElementTypes():
        raise errors.InvalidElementError
      self[element] *= m