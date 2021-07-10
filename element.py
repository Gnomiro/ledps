import error

import numpy

elements = ['physical', 'poison']

def getValidElements():
  return elements

class ElementContainer():
  """docstring for ElementContainer"""
  def __init__(self, default_ = 0, **elements_):

    self._element = dict.fromkeys(getValidElements(), default_)

    for element, value in elements_.items():
      if element not in getValidElements():
        raise error.InvalidElement(element)
      self._element[element] = self._element[element] + value

  def __str__(self):
    info = ''
    for key in self._element.keys():
      info += ('{}: {}, '.format(key, self._element[key]))
    return info[:-2] # remove last comma and space

  def __iadd__(self, other):
    for element in self._element.keys():
      self._element[element] = self._element[element] + other_._element[element]
    return self

  def iaddMultiple(self, *other_):
    for element in self._element.keys():
      for other in other_:
        self._element[element] = self._element[element] + other._element[element]
    return self

  def __add__(self, other):
    result = element.ElementContainer()
    for element in self._element.keys():
      result._element[element] = self._element[element] + other_._element[element]
    return result

  def __isub__(self, other):
    for element in self._element.keys():
      self._element[element] = self._element[element] - other_._element[element]
    return self

  def __sub__(self, other):
    result = element.ElementContainer()
    for element in self._element.keys():
      result._element[element] = self._element[element] - other_._element[element]
    return result

  def iaddValue(self, value_):
    for element in self._element.keys():
      self._element[element] = self._element[element]
    return self

  def addValue(self, value_):
    result = ElementContainer()
    for element in self._element.keys():
      result._element[element] = self._element[element]
    return result

  def imultiply(self, other_, shift_ = 0):
    for element in self._element.keys():
      self._element[element] = self._element[element] * (other_._element[element] + shift_)
    return self

  def multiply(self, other_, shift_ = 0):
    result = ElementContainer()
    for element in self._element.keys():
      result._element[element] = self._element[element] * (other_._element[element] + shift_)
    return result

  def __imul__(self, other_):
    return self.imultiply(other_)

  def __mul__(self, other_):
    return self.multiply(other_)

  def imultiplyByFactor(self, factor_, shift_ = 0.):
    for element in self._element.keys():
      self._element[element] = self._element[element] * (factor_ + shift_)
    return self

  def multiplyByFactor(self, factor_, shift_ = 0.):
    result = ElementContainer()
    for element in self._element.keys():
      result._element[element] = elf._element[element] * (factor_ + shift_)
    return result

  def setUpperLimit(self, limit_):
    for element in self._element.keys():
      self._element[element] = numpy.minimum(self._element[element], limit_)
    return self

  def getSum(self):
    return sum(self._element.values())