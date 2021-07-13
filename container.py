import error

from print_dict import pd

_attackTypes = ['melee', 'spell', 'throwing', 'bow']
_damageTypes = ['curse', 'dot', 'hit']
_elementTypes = ['physical', 'fire', 'poison', 'cold', 'lightning', 'void']
_multiplierTypes = ['increase', 'more']

_durationModifierTypes = ['onHit', 'effect', 'duration']

_attributeTypes = ['strength', 'dexterity', 'intelligence', 'vitality']

######################################################################
######################################################################
# TypeContainers; managing kwargs access and defaultKeys
######################################################################
######################################################################

######################################################################
# Base type container
######################################################################

class TypeContainer():
  """docstring for TypeContainer"""
  def __init__(self, keys_, defaultValue_, extrakeys_ = [], defaultKey_ = None):
    self._name = 'typeContainer'

    self._data = {}

    self._keys = keys_ + extrakeys_
    self._defaultValue = defaultValue_
    self._defaultKey = defaultKey_

    pass

  def get(self, **types_):
    k = types_[self._keyName] if self._keyName in types_.keys() else self._defaultKey
    # fall back if container has no default value
    # multiplerContainer implements its own routine to return product of increase and more if nothing is specified
    if k == None:
      result = self._data
    elif k in self._keys:
      # print(k)
      if not isinstance(self._defaultValue, TypeContainer):
      # if isinstance(self._defaultValue, (int, float, complex)) and not isinstance(self._defaultValue, bool):
        result = self._data.get(k, self._defaultValue)
      else:
        result = self._data.get(k, self._defaultValue).get(**types_)

    return result


  def set(self, value_, **types_):
    k = types_[self._keyName] if self._keyName in types_.keys() else self._defaultKey
    # fall back if container has no default value
    # must return an error in this case as a set requires a specific slot!
    if k == None:
      raise error.MissingContainerType(self._name, self._keys, **types_)
    elif k in self._keys:
      # print(k)
      self._data.setdefault(k, self._defaultValue)
      if not isinstance(self._defaultValue, TypeContainer):
      # if isinstance(self._defaultValue, (int, float, complex)) and not isinstance(self._defaultValue, bool):
        self._data[k] = value_
      else:
        self._data[k].set(value_ = value_, **types_)

  # human readable
  def __str__(self):
    return self._data.__str__()

  # general string representation
  def __repr__(self):
    return self._data.__repr__()

######################################################################
# Attack type container
######################################################################

class AttackTypeContainer(TypeContainer):
  """docstring for AttackTypeContainer"""
  def __init__(self, defaultValue_ = 0, extrakeys_ = [], defaultKey_ = None,):
    super(AttackTypeContainer, self).__init__(keys_ = _attackTypes, defaultValue_ = defaultValue_, extrakeys_ = extrakeys_, defaultKey_ = defaultKey_)
    self._name = 'attackTypeContainer'
    self._keyName = 'attackType_'
    # self._defaultKey = 'generic'

######################################################################
# Element type container
######################################################################

class ElementTypeContainer(TypeContainer):
  """docstring for ElementTypeContainer"""
  def __init__(self, defaultValue_ = 0, extrakeys_ = [], defaultKey_ = None,):
    super(ElementTypeContainer, self).__init__(keys_ = _elementTypes, defaultValue_ = defaultValue_, extrakeys_ = extrakeys_, defaultKey_ = defaultKey_)
    self._name = 'elementTypeContainer'
    self._keyName = 'elementType_'

######################################################################
# Damage type container
######################################################################

class DamageTypeContainer(TypeContainer):
  """docstring for DamageTypeContainer"""
  def __init__(self, defaultValue_ = 0, extrakeys_ = [], defaultKey_ = None,):
    super(DamageTypeContainer, self).__init__(keys_ = _damageTypes, defaultValue_ = defaultValue_, extrakeys_ = extrakeys_, defaultKey_ = defaultKey_)
    self._name = 'damageTypeContainer'
    self._keyName = 'damageType_'

######################################################################
# Attribute type container
######################################################################

class AttributeTypeContainer(TypeContainer):
  """docstring for AttributeTypeContainer"""
  def __init__(self, defaultValue_ = 0, extrakeys_ = [], defaultKey_ = None,):
    super(AttributeTypeContainer, self).__init__(keys_ = _attributeTypes, defaultValue_ = defaultValue_, extrakeys_ = extrakeys_, defaultKey_ = defaultKey_)
    self._name = 'attributeTypeContainer'

######################################################################
# Multiplier type container
# must always be last container
######################################################################

class MultiplierTypeContainer(TypeContainer):
  """docstring for MultiplierTypeContainer"""
  def __init__(self):
    super(MultiplierTypeContainer, self).__init__(keys_ = _multiplierTypes, defaultValue_ = 0)
    self._name = 'multiplierTypeContainer'
    self._keyName = 'multiplierType_'
    self._data['more'] = 1.
    self._data['increase'] = 0.

  def get(self, **types_):
    k = types_[self._keyName] if self._keyName in types_.keys() else self._defaultKey
    # multiplerContainer implements its own routine to dict of no key is required
    if k == None:
      result = self._data
    elif k in self._keys:
      result = self._data[k]

    return result

######################################################################
# DurationModifer type container
######################################################################

class DurationModifierTypeContainer(TypeContainer):
  """docstring for DurationModifierTypeContainer"""
  def __init__(self):
    super(DurationModifierTypeContainer, self).__init__(keys_ = _durationModifierTypes, defaultValue_ = MultiplierTypeContainer())
    self._name = 'durationModiferTypeContainer'
    self._keyName = 'durationModifierType_'
    self._data['onHit'] = AttackTypeContainer(extrakeys_ = ['generic'], defaultKey_ = 'generic', defaultValue_ = MultiplierTypeContainer())

######################################################################
######################################################################
# Implementations
######################################################################
######################################################################

######################################################################
# Base implementations class
######################################################################

class ContainerImplementation():
  """docstring for ContainerImplementation"""
  def get(self, **types_):
    return self._container.get(**types_)

  def set(self, value_, **types_):
    self._container.set(value_, **types_)

  def __str__(self):
    return self._container.__str__()

  def __repr__(self):
    return self._container.__repr__()

######################################################################
# Attribute container class
######################################################################

class AttributeContainer(ContainerImplementation):
  """docstring for AttributeContainer"""
  def __init__(self, defaultValue_ = 0):
    self._container = AttributeTypeContainer(defaultValue_ = defaultValue_)

######################################################################
# Resistance container class
######################################################################

class ResistanceContainer(ContainerImplementation):
  """docstring for ResistanceContainer"""
  def __init__(self, defaultValue_ = 0):
    self._container = ElementTypeContainer(defaultValue_ = defaultValue_)

######################################################################
# Penetration container class; same as ResistanceContainer
######################################################################

class PenetrationContainer(ContainerImplementation):
  """docstring for PenetrationContainer"""
  def __init__(self, defaultValue_ = 0):
    self._container = ElementTypeContainer(defaultValue_ = defaultValue_)

######################################################################
# DurationModifer container class
######################################################################

class DurationModifierContainer(ContainerImplementation):
  """docstring for DurationModifierContainer"""
  def __init__(self):
    self._container = DurationModifierTypeContainer()

######################################################################
# Multiplier container class
######################################################################

class MultiplierContainer(ContainerImplementation):
  """docstring for MultiplierContainer"""
  def __init__(self):
    self._container = AttackTypeContainer(extrakeys_ = ['generic'], defaultKey_ = 'generic', defaultValue_ = DamageTypeContainer(extrakeys_ = ['generic'], defaultKey_ = 'generic', defaultValue_ = ElementTypeContainer(extrakeys_ = ['generic'], defaultKey_ = 'generic', defaultValue_ = MultiplierTypeContainer())))
