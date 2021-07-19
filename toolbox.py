import error

def validateInput(name_, required_, **provided_):

  # test if all required entries are provided by provided_
  if not all([r in provided_.keys() for r in required_]):
    raise error.MissingDurationArgument(name_, required_, **provided_) from None

def prettifyModifier(modifier):
  s = str(modifier)
  result = ''
  tab = ' ' * 4
  nt = 1
  p = 0
  for i, k in enumerate(s):
    if s[i:i+3] == ': {':
      result += s[p:i+1] + '\n' + tab*nt
      p = i + 1
      nt += 1
    if k == '}':
      nt -= 1
    if k == ',':
      result += s[p:i+1] + '\n' + tab*(nt-1)
      p = i + 1
  result += s[p:]
  return result

######################################################################
# More class which overrides addition to multiplication for mergin more multipliers
######################################################################

class More(object):
  """docstring for More"""
  def __init__(self, value_ = 0):
    self._value = 1. + value_
    pass

  def __add__(self, other_):
    result = More()
    result._value = self._value * other_._value
    return result

  def __sub__(self, other_):
    result = More()
    result._value = self._value / other_._value
    return result

  # this is for scalar multiplication from outside (ring-structure) and thus other must be shifted back after initial construction
  # python does not allow for the definition of __imult__ between two different types; as far as I know
  def __imul__(self, other_):
    self._value = (self._value - 1.) * (other_._value - 1.) + 1.
    # self._value = 2 * self._value - 1. - self._value * other_._value + other_._value
    return self

  def __eq__(self, other_):
    return self._value == other_._value

  def __repr__(self):
    return self._value.__repr__()

  def __str__(self):
    return self._value.__str__()