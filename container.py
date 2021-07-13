import error

import copy

from toolbox import More

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

  def getDefaultValue(self, key):
    return self._defaultValue

  def get(self, **types_):
    k = types_[self._keyName] if self._keyName in types_.keys() else self._defaultKey
    # if no suitable argument was passed and no defaulKey is available raise an exceptions
    if k == None and k not in self._keys:
      raise error.MissingContainerType(self._name, self._keys, **types_)
    else:
      # print(k)
      if not isinstance(self.getDefaultValue(k), TypeContainer):
        result = self._data.get(k, self.getDefaultValue(k))
      else:
        result = self._data.get(k, self.getDefaultValue(k)).get(**types_)

    return result

  def set(self, value_, **types_):
    k = types_[self._keyName] if self._keyName in types_.keys() else self._defaultKey
    # fall back if container has no default value
    # must return an error in this case as a set requires a specific slot!
    if k == None:
      raise error.MissingContainerType(self._name, self._keys, **types_)
    elif k in self._keys:
      # print(k)
      self._data.setdefault(k, copy.deepcopy(self.getDefaultValue(k)))
      if not isinstance(self.getDefaultValue(k), TypeContainer):
        self._data[k] = type(self.getDefaultValue(k))(value_)
      else:
        self._data[k].set(value_ = value_, **types_)
    pass

  def _add(self, left_, right_):

    for i in set(left_._data.keys()) | set(right_._data.keys()):
      key = {self._keyName: i}
      if (i in left_._data.keys() and not isinstance(left_._data.get(i), TypeContainer)) or (i in right_._data.keys() and not isinstance(right_._data.get(i), TypeContainer)):
        key = {self._keyName: i}
        self._data[i] = left_.get(**key) + right_.get(**key)
      else:
        self._data[i] = copy.deepcopy(self.getDefaultValue(i))
        self._data[i]._add(left_._data.get(i, copy.deepcopy(left_.getDefaultValue(i))), right_._data.get(i, copy.deepcopy(right_.getDefaultValue(i))))
    pass

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
  def __init__(self, defaultValue_ = 0., extrakeys_ = [], defaultKey_ = None,):
    super(AttackTypeContainer, self).__init__(keys_ = _attackTypes, defaultValue_ = defaultValue_, extrakeys_ = extrakeys_, defaultKey_ = defaultKey_)
    self._name = 'attackTypeContainer'
    self._keyName = 'attackType_'
    pass

######################################################################
# Element type container
######################################################################

class ElementTypeContainer(TypeContainer):
  """docstring for ElementTypeContainer"""
  def __init__(self, defaultValue_ = 0., extrakeys_ = [], defaultKey_ = None,):
    super(ElementTypeContainer, self).__init__(keys_ = _elementTypes, defaultValue_ = defaultValue_, extrakeys_ = extrakeys_, defaultKey_ = defaultKey_)
    self._name = 'elementTypeContainer'
    self._keyName = 'elementType_'
    pass

######################################################################
# Damage type container
######################################################################

class DamageTypeContainer(TypeContainer):
  """docstring for DamageTypeContainer"""
  def __init__(self, defaultValue_ = 0., extrakeys_ = [], defaultKey_ = None,):
    super(DamageTypeContainer, self).__init__(keys_ = _damageTypes, defaultValue_ = defaultValue_, extrakeys_ = extrakeys_, defaultKey_ = defaultKey_)
    self._name = 'damageTypeContainer'
    self._keyName = 'damageType_'
    pass

######################################################################
# Attribute type container
######################################################################

class AttributeTypeContainer(TypeContainer):
  """docstring for AttributeTypeContainer"""
  def __init__(self, defaultValue_ = 0., extrakeys_ = [], defaultKey_ = None,):
    super(AttributeTypeContainer, self).__init__(keys_ = _attributeTypes, defaultValue_ = defaultValue_, extrakeys_ = extrakeys_, defaultKey_ = defaultKey_)
    self._name = 'attributeTypeContainer'
    self._keyName = 'attributeType_'
    pass

######################################################################
# Multiplier type container
# must always be last container
######################################################################

class MultiplierTypeContainer(TypeContainer):
  """docstring for MultiplierTypeContainer"""
  def __init__(self):
    super(MultiplierTypeContainer, self).__init__(keys_ = _multiplierTypes, defaultValue_ = 0.)
    self._name = 'multiplierTypeContainer'
    self._keyName = 'multiplierType_'
    self._data['more'] = More(1.)
    pass

  def getDefaultValue(self, key):
    if key != 'more':
      return super().getDefaultValue(key)
    return More(1.)

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
    pass

  def getDefaultValue(self, key):
    if key != 'onHit':
      return super().getDefaultValue(key)
    return AttackTypeContainer(extrakeys_ = ['generic'], defaultKey_ = 'generic', defaultValue_ = MultiplierTypeContainer())

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
    pass

  def __iadd__(self, other_):
    super().__iadd__(other_)
    return self

  def __add__(self, other_, result_):
    result_._container._add(self._container, other_._container)
    return result_

  def __str__(self):
    return self._container.__str__()

  def __repr__(self):
    return self._container.__repr__()

######################################################################
# Attribute container class
######################################################################

class AttributeContainer(ContainerImplementation):
  """docstring for AttributeContainer"""
  def __init__(self, defaultValue_ = 0.):
    self._container = AttributeTypeContainer(defaultValue_ = defaultValue_)
    pass

  def __add__(self, other_):
    result = AttributeContainer(defaultValue_ = self._container._defaultValue + other_._container._defaultValue)
    super().__add__(other_, result)
    return result

######################################################################
# Resistance container class
######################################################################

class ResistanceContainer(ContainerImplementation):
  """docstring for ResistanceContainer"""
  def __init__(self, defaultValue_ = 0.):
    self._container = ElementTypeContainer(defaultValue_ = defaultValue_)
    pass

  def __add__(self, other_):
    result = ResistanceContainer(defaultValue_ = self._container._defaultValue + other_._container._defaultValue)
    super().__add__(other_, result)
    return result

######################################################################
# Penetration container class; same as ResistanceContainer
######################################################################

class PenetrationContainer(ContainerImplementation):
  """docstring for PenetrationContainer"""
  def __init__(self, defaultValue_ = 0.):
    self._container = ElementTypeContainer(defaultValue_ = defaultValue_)

  def __add__(self, other_):
    result = PenetrationContainer(defaultValue_ = self._container._defaultValue + other_._container._defaultValue)
    super().__add__(other_, result)
    return result

######################################################################
# DurationModifer container class
######################################################################

class DurationModifierContainer(ContainerImplementation):
  """docstring for DurationModifierContainer"""
  def __init__(self):
    self._container = DurationModifierTypeContainer()

  def __add__(self, other_):
    result = DurationModifierContainer()
    super().__add__(other_, result)
    return result

######################################################################
# Multiplier container class
######################################################################

class MultiplierContainer(ContainerImplementation):
  """docstring for MultiplierContainer"""
  def __init__(self):
    self._container = AttackTypeContainer(extrakeys_ = ['generic'], defaultKey_ = 'generic', defaultValue_ = DamageTypeContainer(extrakeys_ = ['generic'], defaultKey_ = 'generic', defaultValue_ = ElementTypeContainer(extrakeys_ = ['generic'], defaultKey_ = 'generic', defaultValue_ = MultiplierTypeContainer())))
    pass

  def __add__(self, other_):
    result = MultiplierContainer()
    super().__add__(other_, result)
    return result