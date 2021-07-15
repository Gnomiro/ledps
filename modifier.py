from numpy import product as prod, sum
import copy

import container

from numpy import product
from itertools import chain

import toolbox

############################################################################################
############################################################################################
# Modifier collection class
############################################################################################
############################################################################################

class Modifier():
  """docstring for Modifier"""

  def __init__(self):
    self._multiplier = container.MultiplierContainer()
    self._penetration = container.PenetrationContainer()
    self._attribute = container.AttributeContainer()
    self._duration = {}
    self._trigger = {}
    pass

  def __iadd__(self, other_):
    self._multiplier += other_._multiplier
    self._penetration += other_._penetration
    self._attribute += other_._attribute

    for name in other_._duration.keys():
      if name not in self._duration.keys():
        self._duration[name] = container.DurationModifierContainer()
      self._duration[name] += other_._duration[name]

    for name in other_._trigger.keys():
      if name not in self._trigger.keys():
        self._trigger[name] = container.DurationModifierContainer()
      self._trigger[name] += other_._trigger[name]

    return self

  # copies values from other modifier object; values already present in self are set to default
  def copyFrom(self, other_):
    self._multiplier.copyFrom(other_._multiplier)
    self._penetration.copyFrom(other_._penetration)
    self._attribute.copyFrom(other_._attribute)

    for name in other_._duration.keys():
      if name not in self._duration.keys():
        self._duration[name] = container.DurationModifierContainer()
      self._duration[name].copyFrom(other_._duration[name])

    for name in other_._trigger.keys():
      if name not in self._trigger.keys():
        self._trigger[name] = container.DurationModifierContainer()
      self._trigger[name].copyFrom(other_._trigger[name])

    return self

  def reset(self):
    self._multiplier.reset()
    self._penetration.reset()
    self._attribute.reset()

    for name in self._duration.keys():
      self._duration[name].reset()

    for name in self._trigger.keys():
      self._trigger[name].reset()

  def __add__(self, other_):
    total = Modifier()
    total += self
    total += other_
    return total

  def iaddMultiple(self, *other_):
    for other in other_:
      self += other
    return self

  def scaleByFactor(self, factor_):
    self._multiplier.scaleByFactor(factor_)
    self._penetration.scaleByFactor(factor_)
    self._attribute.scaleByFactor(factor_)

    for name in self._duration.keys():
      self._duration[name].scaleByFactor(factor_)

    for name in self._trigger.keys():
      self._trigger[name].scaleByFactor(factor_)

    return self

  def __str__(self):
    return 'multiplier:\n' + str(self._multiplier) + '\npenetration:\n' + str(self._penetration) + '\nattribute:\n' + str(self._attribute) + '\nduration:\n' + str(self._duration) + '\ntrigger:\n' + str(self._trigger)

  def show(self):
    print('multiplier:')
    print(toolbox.prettifyModifier(self._multiplier))
    print('penetration:')
    print(toolbox.prettifyModifier(self._penetration))
    print('attribute:')
    print(toolbox.prettifyModifier(self._attribute))
    print('duration:')
    print(toolbox.prettifyModifier(self._duration))
    print('trigger:')
    print(toolbox.prettifyModifier(self._trigger))

  def getMultipliers(self):
    return self._multiplier

  def getPenetrations(self):
    return self._penetration

  def getAttributes(self):
    return self._attribute

  def getDurations(self):
    return self._duration

  def getTriggers(self):
    return self._trigger

  def getMultiplier(self, *args_, **kwargs_):
    types = container.convertToTypes(*args_, default_ = {'elementType_': None, 'attackType_': None, 'damageType_': None}, **kwargs_)
    return (1. + self.getIncrease(**types)) * self.getMore(**types)

  def getIncrease(self, *args_, **kwargs_):

    types = container.convertToTypes(*args_, default_ = {'elementType_' : None, 'attackType_': None, 'damageType_': None}, **kwargs_, multiplierType_ = 'increase')

    contributing = []
    contributing.append(copy.deepcopy(types))

    k = 1
    if types['attackType_'] is not None:
      contributing.extend(copy.deepcopy(contributing))
      for i in range(k):
        contributing[i]['attackType_'] = 'generic'
      k *= 2
    if types['damageType_'] is not None:
      contributing.extend(copy.deepcopy(contributing))
      for i in range(k):
        contributing[i]['damageType_'] = 'generic'
      k *= 2
    if types['elementType_'] is not None:
      contributing.extend(copy.deepcopy(contributing))
      for i in range(k):
        contributing[i]['elementType_'] = 'generic'

    sum = 0
    for l in contributing:
      sum += self._multiplier.get(**l)

    return sum

  def getMore(self, *args_, **kwargs_):

    types = container.convertToTypes(*args_, default_ = {'elementType_' : None, 'attackType_': None, 'damageType_': None}, **kwargs_, multiplierType_ = 'more')

    contributing = []
    contributing.append(copy.deepcopy(types))

    k = 1
    if types['attackType_'] is not None:
      contributing.extend(copy.deepcopy(contributing))
      for i in range(k):
        contributing[i]['attackType_'] = 'generic'
      k *= 2
    if types['damageType_'] is not None:
      contributing.extend(copy.deepcopy(contributing))
      for i in range(k):
        contributing[i]['damageType_'] = 'generic'
      k *= 2
    if types['elementType_'] is not None:
      contributing.extend(copy.deepcopy(contributing))
      for i in range(k):
        contributing[i]['elementType_'] = 'generic'

    prod = 1
    for l in contributing:
      # More modifier are stored as an Object of type More; _value is the float representation
      prod *= self._multiplier.get(**l)._value

    return prod

  def getPenetration(self, *args_, **kwargs_):
    types = container.convertToTypes(*args_, **kwargs_)
    return self._penetration.get(**types)

  def getAttribute(self, *args_, **kwargs_):
    types = container.convertToTypes(*args_, **kwargs_)
    return self._attribute.get(**types)

  def getDurationMultiplier(self, name_, *args_, **kwargs_):
    types = container.convertToTypes(*args_, **kwargs_)
    return (1. + self.getDurationIncrease(name_ = name_, **types)) * self.getDurationMore(name_ = name_, **types)

  def getDurationIncrease(self, name_, *args_, **kwargs_):
    if name_ not in self._duration.keys():
      return 0
    types = container.convertToTypes(*args_, default_ = {'attackType_': None}, **kwargs_, multiplierType_ = 'increase')
    sum = self._duration[name_].get(**types)
    if types['attackType_'] != None:
      types['attackType_'] = 'generic'
      sum += self._duration[name_].get(**types)
    return sum

  def getDurationMore(self, name_, *args_, **kwargs_):
    if name_ not in self._duration.keys():
      return 1
    types = container.convertToTypes(*args_, default_ = {'attackType_': None}, **kwargs_, multiplierType_ = 'more')
    prod = self._duration[name_].get(**types)._value
    if types['attackType_'] != None:
      types['attackType_'] = 'generic'
      prod *= self._duration[name_].get(**types)._value
    return prod

  def getTriggerMultiplier(self, name_, *args_, **kwargs_):
    types = container.convertToTypes(*args_, **kwargs_)
    return (1. + self.getTriggerIncrease(name_ = name_, **types)) * self.getTriggerMore(name_ = name_, **types)

  def getTriggerIncrease(self, name_, *args_, **kwargs_):
    if name_ not in self._trigger.keys():
      return 0
    types = container.convertToTypes(*args_, default_ = {'attackType_': None}, **kwargs_, multiplierType_ = 'increase')
    sum = self._trigger[name_].get(**types)
    if types['attackType_'] is not None:
      types['attackType_'] = 'generic'
      sum += self._trigger[name_].get(**types)
    return sum

  def getTriggerMore(self, name_, *args_, **kwargs_):
    if name_ not in self._trigger.keys():
      return 1
    types = container.convertToTypes(*args_, default_ = {'attackType_': None}, **kwargs_, multiplierType_ = 'more')
    prod = self._trigger[name_].get(**types)._value
    if types['attackType_'] is not None:
      types['attackType_'] = 'generic'
      prod *= self._trigger[name_].get(**types)._value
    return prod

  def addIncrease(self, value_, *args_, **kwargs_):
    types = container.convertToTypes(*args_, default_ = {'attackType_': 'generic', 'damageType_': 'generic'}, **kwargs_, multiplierType_ = 'increase')
    self._multiplier.add(value_ = value_, **types)

  def addMore(self, value_, *args_, **kwargs_):
    types = container.convertToTypes(*args_, default_ = {'attackType_': 'generic', 'damageType_': 'generic'}, **kwargs_, multiplierType_ = 'more')
    self._multiplier.add(value_ = value_, **types)

  def addPenetration(self, value_, *args_, **kwargs_):
    types = container.convertToTypes(*args_, **kwargs_)
    self._penetration.add(value_ = value_, **types)

  def addAttribute(self, value_, *args_, **kwargs_):
    types = container.convertToTypes(*args_, **kwargs_)
    self._attribute.add(value_, **types)

  def addDuration(self, name_, value_, *args_, **kwargs_):
    types = container.convertToTypes(*args_, default_ = {'attackType_': 'generic', 'multiplierType_': 'increase'}, **kwargs_)
    if name_ not in self._duration.keys():
      self._duration[name_] = container.DurationModifierContainer()
    self._duration[name_].add(value_ = value_, **types)

  def addTrigger(self, name_, value_, *args_, **kwargs_):
    types = container.convertToTypes(*args_, default_ = {'attackType_': 'generic', 'multiplierType_': 'increase'}, **kwargs_)
    if name_ not in self._trigger.keys():
      self._trigger[name_] = container.DurationModifierContainer()
    self._trigger[name_].add(value_ = value_, **types)

  def setIncrease(self, value_, *args_, **kwargs_):
    types = container.convertToTypes(*args_, default_ = {'attackType_': 'generic', 'damageType_': 'generic'}, **kwargs_, multiplierType_ = 'increase')
    self._multiplier.set(value_ = value_, **types)

  def setMore(self, value_, *args_, **kwargs_):
    types = container.convertToTypes(*args_, default_ = {'attackType_': 'generic', 'damageType_': 'generic'}, **kwargs_, multiplierType_ = 'more')
    self._multiplier.set(value_ = value_, **types)

  def setPenetration(self, value_, *args_, **kwargs_):
    types = container.convertToTypes(*args_, **kwargs_)
    self._penetration.set(value_ = value_, **types)

  def setAttribute(self, value_, *args_, **kwargs_):
    types = container.convertToTypes(*args_, **kwargs_)
    self._attribute.set(value_, **types)

  def setDuration(self, name_, value_, *args_, **kwargs_):
    types = container.convertToTypes(*args_, default_ = {'attackType_': 'generic', 'multiplierType_': 'increase'}, **kwargs_)
    if name_ not in self._duration.keys():
      self._duration[name_] = container.DurationModifierContainer()
    self._duration[name_].set(value_ = value_, **types)

  def setTrigger(self, name_, value_, *args_, **kwargs_):
    types = container.convertToTypes(*args_, default_ = {'attackType_': 'generic', 'multiplierType_': 'increase'}, **kwargs_)
    if name_ not in self._trigger.keys():
      self._trigger[name_] = container.DurationModifierContainer()
    self._trigger[name_].set(value_ = value_, **types)

  def fromBuff(self, durationContainer_):
    self.reset()
    for buff in durationContainer_.getActiveWithType('buff'):
      self += buff.getModifier()

    return self

############################################################################################
# Additional constructor functions
############################################################################################

def fromBuff(durationContainer_):
  modifier = Modifier()
  for buff in durationContainer_.getActiveWithType('buff'):
    modifier += buff.getModifier()

  return modifier


class ModifierChain():
  """docstring for ModifierChain"""
  def __init__(self, *args_):
    self._data = []
    for k in args_:
      if isinstance(k, ModifierChain):
        # print('chain')
        self._data.extend(k._data)
      else:
        # print('no chain')
        self._data.append(k)
    pass

  # def __iadd__(self, other_):
  #   self._data.append(other_)
  #   return self

  # def __add__(self, other_):
  #   new = ModifierChain()
  #   print(type(self))
  #   print(type(other_))
  #   new._data = self._data
  #   new._data.append(other_)
  #   return new

  def merge(self):
    modifier = Modifier()
    for k in self._data:
      modifier += k
    return modifier

  def getMultipliers(self):
    return self._multiplier

  def getPenetrations(self):
    return self._penetration

  def getAttributes(self):
    return self._attribute

  def getDurationKeys(self):
    keys = set()
    for k in self._data:
      keys =  keys | set(k.getDurations().keys())
    return keys

  def getTriggerKeys(self):
    keys = set()
    for k in self._data:
      keys =  keys | set(k.getTriggers().keys())
    return keys

  def getMultiplier(self, *args_, **kwargs_):
    return (1. + self.getIncrease(*args_, **kwargs_)) * self.getMore(*args_, **kwargs_)

  def getIncrease(self, *args_, **kwargs_):
    return sum([k.getIncrease(*args_, **kwargs_) for k in self._data])

  def getMore(self, *args_, **kwargs_):
    return product([k.getMore(*args_, **kwargs_) for k in self._data])

  def getPenetration(self, *args_, **kwargs_):
    return sum([k.getPenetration(*args_, **kwargs_) for k in self._data])

  def getAttribute(self, *args_, **kwargs_):
    return sum([k.getAttribute(*args_, **kwargs_) for k in self._data])

  def getDurationMultiplier(self, name_, *args_, **kwargs_):
    return (1. + self.getDurationIncrease(name_, *args_, **kwargs_)) * self.getDurationMore(name_, *args_, **kwargs_)

  def getDurationIncrease(self, name_, *args_, **kwargs_):
    return sum([k.getDurationIncrease(name_, *args_, **kwargs_) for k in self._data])

  def getDurationMore(self, name_, *args_, **kwargs_):
    return product([k.getDurationMore(name_, *args_, **kwargs_) for k in self._data])

  def getTriggerMultiplier(self, name_, *args_, **kwargs_):
    return (1. + self.getTriggerIncrease(name_, *args_, **kwargs_)) * self.getTriggerMore(name_, *args_, **kwargs_)

  def getTriggerIncrease(self, name_, *args_, **kwargs_):
    return sum([k.getTriggerIncrease(name_, *args_, **kwargs_) for k in self._data])

  def getTriggerMore(self, name_, *args_, **kwargs_):
    return product([k.getTriggerMore(name_, *args_, **kwargs_) for k in self._data])


