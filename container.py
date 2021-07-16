import error

import copy, itertools, error

from toolbox import More

from print_dict import pd

_categoryTypes = ['damage', 'speed']
_attackTypes = ['melee', 'spell', 'throwing', 'bow']
_damageTypes = ['curse', 'dot', 'hit']
_elementTypes = ['physical', 'fire', 'cold', 'lightning', 'void', 'necrotic', 'poison']
_multiplierTypes = ['increase', 'more']

_durationModifierTypes = ['onHit', 'effect', 'duration']

_attributeTypes = ['strength', 'dexterity', 'intelligence', 'vitality', 'attunement']

_validArguments = [*_attackTypes, *_damageTypes, *_elementTypes, *_multiplierTypes, *_durationModifierTypes, *_attackTypes, *_attributeTypes, *_categoryTypes, *['generic', None]]

def isValidArgument(key, validArguments_ = _validArguments):
  supported = key in validArguments_
  if not supported:
    print('Unsupport keyword \'{}\' provided and ignored.'.format(key))
  return supported

def convertToTypes(*args_, default_ = {}, **kwargs_):
  parsed = {}
  for d in default_.keys():
    if isValidArgument(default_[d]):
      parsed[d] = default_[d]
  for k in args_:
    if not isValidArgument(k):
      continue
    elif k in _categoryTypes:
      parsed['categoryType_'] = k
    elif k in _attackTypes:
      parsed['attackType_'] = k
    elif k in _damageTypes:
      parsed['damageType_'] = k
    elif k in _elementTypes:
      parsed['elementType_'] = k
    elif k in _multiplierTypes:
      parsed['multiplierType_'] = k
    elif k in _attributeTypes:
      parsed['attributeType_'] = k
    elif k in _durationModifierTypes:
      parsed['durationModifierType_'] = k
  for d in kwargs_.keys():
    if isValidArgument(kwargs_[d]):
      parsed[d] = kwargs_[d]
  return parsed

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
  def __init__(self, keys_, defaultValue_, extrakeys_ = [], defaultKey_ = None, **kwargs_):
    self._name = 'typeContainer'

    self._data = {}

    self._keys = keys_ + extrakeys_
    self._defaultValue = defaultValue_
    self._defaultKey = defaultKey_

    for e, v in kwargs_.items():
      if isValidArgument(e, self._keys):
          self._data[e] = v
    pass

  def getDefaultValue(self, key):
    return self._defaultValue

  def copyDefaultValue(self, key):
    return copy.deepcopy(self.getDefaultValue(key))

  def get(self, **types_):
    # todo: if something is not present the default value of the deepest base object could be returned
    k = types_[self._keyName] if self._keyName in types_.keys() and types_[self._keyName] != None else self._defaultKey
    # if no suitable argument was passed and no defaulKey is available raise an exceptions
    if k == None and k not in self._keys:
      raise error.MissingContainerType(self._name, self._keys, **types_)
    else:
      if not isinstance(self.getDefaultValue(k), TypeContainer):
        # result = self._data.get(k, self.getDefaultValue(k))
        result = (self._data[k] if k in self._data else self.getDefaultValue(k))
      else:
        # result = self._data.get(k, self.getDefaultValue(k)).get(**types_)
        result = (self._data[k] if k in self._data else self.getDefaultValue(k)).get(**types_)

    return result

  def set(self, value_, **types_):
    k = types_[self._keyName] if self._keyName in types_.keys() and types_[self._keyName] != None else self._defaultKey
    # fall back if container has no default value
    # must return an error in this case as a set requires a specific slot!
    if k == None:
      raise error.MissingContainerType(self._name, self._keys, **types_)
    elif k in self._keys:
      self._data.setdefault(k, self.copyDefaultValue(k))
      if not isinstance(self.getDefaultValue(k), TypeContainer):
        t = type(self.getDefaultValue(k))
        self._data[k] = value_ if type(value_) is t else t(value_)
      else:
        self._data[k].set(value_ = value_, **types_)
    pass

  # positions are switched here. self is the empty object wich receives the sum from left_ and right_
  def _add(self, left_, right_):
    for i in set(left_._data.keys()) | set(right_._data.keys()):
      key = {self._keyName: i}
      if (i in left_._data and not isinstance(left_._data.get(i), TypeContainer)) or (i in right_._data and not isinstance(right_._data.get(i), TypeContainer)):
        self._data[i] = left_.get(**key) + right_.get(**key)
      else:
        if i not in self._data:
          self._data[i] = self.copyDefaultValue(i)
        self._data[i]._add(left_._data.get(i, (left_.getDefaultValue(i))), right_._data.get(i, (right_.getDefaultValue(i))))
    return self

  def _iadd(self, other_):

    for i in set(other_._data.keys()) | set(self._data.keys()):
      key = {self._keyName: i}
      if i not in self._data:
        self._data[i] = self.copyDefaultValue(i)
      if (i in self._data and not isinstance(self._data.get(i), TypeContainer)) or (i in other_._data and not isinstance(other_._data.get(i), TypeContainer)):
        self._data[i] += other_.get(**key)
      else:
        if i in other_._data:
          self._data[i]._iadd(other_._data[i])
    return self

  def iaddIgnoreDefault(self, other_):

    for i in other_._data.keys():
      key = {self._keyName: i}
      if i not in self._data:
        self._data[i] = self.copyDefaultValue(i)
      if not isinstance(other_._data[i], TypeContainer):
        self._data[i] += other_.get(**key)
      else:
        self._data[i].iaddIgnoreDefault(other_._data[i])
    return self

  def iscaleByFactor(self, factor_):
    for i in self._data:
      key = {self._keyName: i}
      if not isinstance(self._data.get(i), TypeContainer):
        t = type(self.getDefaultValue(i))
        self._data[i] *= factor_ if type(factor_) is t else t(factor_)
      else:
        self._data[i].iscaleByFactor(factor_)
    pass

  def reset(self):
    for i in self._data:
      key = {self._keyName: i}
      if not isinstance(self._data.get(i), TypeContainer):
        self._data[i] = self.getDefaultValue(i)
      else:
        self._data[i].reset()
    pass

  def copyFrom(self, other_):
    for i in set(other_._data.keys()) | set(self._data.keys()):
      key = {self._keyName: i}
      if (i in self._data and not isinstance(self._data.get(i), TypeContainer)) or (i in other_._data and not isinstance(other_._data.get(i), TypeContainer)):
        if i not in self._data:
          self._data[i] = self.copyDefaultValue(i)
        if i in other_._data:
          self._data[i] = other_.get(**key)
        else:
          self._data[i] = self.getDefaultValue(i)
      else:
        if i not in self._data:
          self._data[i] = self.copyDefaultValue(i)
        self._data[i].copyFrom(other_._data.get(i, other_.getDefaultValue(i)))
    return self

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
  def __init__(self, defaultValue_ = 0., extrakeys_ = [], defaultKey_ = None, **kwargs_):
    super(AttackTypeContainer, self).__init__(keys_ = _attackTypes, defaultValue_ = defaultValue_, extrakeys_ = extrakeys_, defaultKey_ = defaultKey_, **kwargs_)
    self._name = 'attackTypeContainer'
    self._keyName = 'attackType_'
    pass

######################################################################
# Element type container
######################################################################

class ElementTypeContainer(TypeContainer):
  """docstring for ElementTypeContainer"""
  def __init__(self, defaultValue_ = 0., extrakeys_ = [], defaultKey_ = None, **kwargs_):
    super(ElementTypeContainer, self).__init__(keys_ = _elementTypes, defaultValue_ = defaultValue_, extrakeys_ = extrakeys_, defaultKey_ = defaultKey_, **kwargs_)
    self._name = 'elementTypeContainer'
    self._keyName = 'elementType_'
    pass

######################################################################
# Damage type container
######################################################################

class DamageTypeContainer(TypeContainer):
  """docstring for DamageTypeContainer"""
  def __init__(self, defaultValue_ = 0., extrakeys_ = [], defaultKey_ = None, **kwargs_):
    super(DamageTypeContainer, self).__init__(keys_ = _damageTypes, defaultValue_ = defaultValue_, extrakeys_ = extrakeys_, defaultKey_ = defaultKey_, **kwargs_)
    self._name = 'damageTypeContainer'
    self._keyName = 'damageType_'
    pass

######################################################################
# Attribute type container
######################################################################

class AttributeTypeContainer(TypeContainer):
  """docstring for AttributeTypeContainer"""
  def __init__(self, defaultValue_ = 0., extrakeys_ = [], defaultKey_ = None, **kwargs_):
    super(AttributeTypeContainer, self).__init__(keys_ = _attributeTypes, defaultValue_ = defaultValue_, extrakeys_ = extrakeys_, defaultKey_ = defaultKey_, **kwargs_)
    self._name = 'attributeTypeContainer'
    self._keyName = 'attributeType_'
    pass

######################################################################
# Attribute type container
######################################################################

class CategoryTypeContainer(TypeContainer):
  """docstring for CategoryTypeContainer"""
  def __init__(self, defaultValue_ = 0., extrakeys_ = [], defaultKey_ = None, **kwargs_):
    super(CategoryTypeContainer, self).__init__(keys_ = _categoryTypes, defaultValue_ = defaultValue_, extrakeys_ = extrakeys_, defaultKey_ = defaultKey_, **kwargs_)
    self._name = 'categoryTypeContainer'
    self._keyName = 'categoryType_'
    pass

  def copy(self):
    print('xxxxxxxxxxxx')

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
    # self._data['more'] = More(1.)
    pass

  def getDefaultValue(self, key):
    if key != 'more':
      return super().getDefaultValue(key)
    return More()

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

  def keys(self):
    return self._container._keys

  def __getitem__(self, key):
    if key not in self.keys():
      raise error.InvalidContainerKey(self._container._name, key, *self.keys())
    return self._container.get(**{self._container._keyName : key})

  def __iter__(self):
    for k in self._container._keys:
      yield k

  def __len__(self):
    return len(self._container._keys)

  def get(self, **types_):
    return self._container.get(**types_)

  def set(self, value_, **types_):
    self._container.set(value_, **types_)
    return self

  def add(self, value_, **types_):
    new = self._container.get(**types_)
    if type(new) is not type(value_):
      new += type(new)(value_)
    else:
      new += value_
    return self._container.set(new, **types_)

  def iscaleByFactor(self, factor_):
    self._container.iscaleByFactor(factor_)
    return self

  def reset(self):
    self._container.reset()
    return self

  def copyFrom(self, other_):
    self._container.copyFrom(other_._container)
    return self

  def __iadd__(self, other_):
    self._container._iadd(other_._container)
    return self

  def iaddIgnoreDefault(self, other_):
    self._container.iaddIgnoreDefault(other_._container)
    return self

  # switches around objects to store new values in result
  def __add__(self, other_, result_):
    return result_._container._add(self._container, other_._container)

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

  def __iadd__(self, other_):
    super().__iadd__(other_)
    self._container._defaultValue += other_._container._defaultValue
    return self

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

  def __iadd__(self, other_):
    super().__iadd__(other_)
    self._container._defaultValue += other_._container._defaultValue
    return self

  def __add__(self, other_):
    result = ResistanceContainer(defaultValue_ = self._container._defaultValue + other_._container._defaultValue)
    super().__add__(other_, result)
    return result

######################################################################
# Resistance container class; same as ResistanceContainer
######################################################################

class DamageContainer(ContainerImplementation):
  """docstring for DamageContainer"""
  def __init__(self, defaultValue_ = 0., **kwargs_):
    self._container = ElementTypeContainer(defaultValue_ = defaultValue_, **kwargs_)
    pass

  def __iadd__(self, other_):
    super().__iadd__(other_)
    self._container._defaultValue += other_._container._defaultValue
    return self

  def __add__(self, other_):
    result = DamageContainer(defaultValue_ = self._container._defaultValue + other_._container._defaultValue)
    super().__add__(other_, result)
    return result

######################################################################
# Penetration container class; same as ResistanceContainer
######################################################################

class PenetrationContainer(ContainerImplementation):
  """docstring for PenetrationContainer"""
  def __init__(self, defaultValue_ = 0.):
    self._container = ElementTypeContainer(defaultValue_ = defaultValue_)
    pass

  def __iadd__(self, other_):
    super().__iadd__(other_)
    self._container._defaultValue += other_._container._defaultValue
    return self

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
    self._container = CategoryTypeContainer(defaultKey_ = 'damage', defaultValue_ = AttackTypeContainer(extrakeys_ = ['generic'], defaultKey_ = 'generic', defaultValue_ = DamageTypeContainer(extrakeys_ = ['generic'], defaultKey_ = 'generic', defaultValue_ = ElementTypeContainer(extrakeys_ = ['generic'], defaultKey_ = 'generic', defaultValue_ = MultiplierTypeContainer()))))
    pass

  def __add__(self, other_):
    result = MultiplierContainer()
    super().__add__(other_, result)
    return result