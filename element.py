import error

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

  def imultiplyByFactor(self, factor_, base_ = 0.):
    for element, value in self._element.items():
      self._element[element] = value * (base_ + factor_)
    return self

  def multiplyByFactor(self, factor_, base_ = 0.):
    result = ElementContainer()
    for element, value in self._element.items():
      result._element[element] = value * (base_ + factor_)
    return result

  def getSum(self):
    return sum(self._element.values())