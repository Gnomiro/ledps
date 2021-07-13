import error

def validateInput(name_, required_, **provided_):

  # test if all required entries are provided by provided_
  if not all([r in provided_.keys() for r in required_]):
    raise error.MissingDurationArgument(name_, required_, **provided_) from None

######################################################################
# More class which overrides addition to multiplication for mergin more multipliers
######################################################################

class More(object):
  """docstring for More"""
  def __init__(self, value_ = 1.):
    self._value = value_
    pass

  def __add__(self, other_):
    result = More(1.)
    result._value = self._value * other_._value
    return result

  def __eq__(self, other_):
    return self._value == other_._value

  def __repr__(self):
    return self._value.__repr__()

  def __str__(self):
    return self._value.__str__()