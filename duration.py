import toolbox, error, element, modifier

import copy

import warnings

############################################################################################
############################################################################################
# Duration object base classes
############################################################################################
############################################################################################

############################################################################################
# Duration base
############################################################################################

class Duration():

  """docstring for Duration"""
  def __init__(self, name_, **kwargs_):
    self._types = list()

    self._name = name_

    required = ['duration_', 'maxStacks_']
    toolbox.validateInput(self._name, required, **kwargs_)

    self._permanent = False
    self._elapsed = 0

    self._baseDuration = kwargs_['duration_']
    self._duration = self._baseDuration
    self._maxStacks = kwargs_['maxStacks_']

    self._appliedBy = (None, None)

  def getName(self):
    return self._name

  def hasType(self, type_):
    return type_ in self._types

  def getTypes(self):
    return self._types

  def hasStackLimit(self):
    return self._maxStacks != 0

  def getMaxStacks(self):
    return self._maxStacks

  def setAppliedBy(self, skillName_, skillN_):
    self._appliedBy = (skillName_, skillN_)

  def getAppliedBy(self):
    return self._appliedBy

  def isPermanent(self):
    return self._permanent

  def isActive(self):
    if self.isPermanent():
      return True
    else:
      return self._elapsed < self._duration

  def getRemainingDuration(self):
    return self._duration - self._elapsed

  def applyModifier(self, modifier_):

    self._duration *= (1. + modifier_.getDuration(self._name, 'duration'))
    pass

  def tick(self, timestep_):

    effectiveTimestep = timestep_

    if not self.isPermanent() and self._elapsed + timestep_ >= self._duration:
      # ailment falls off within 'timestep' -> set timestep size and elapsed timer accordingly to acquire accurate damage
      effectiveTimestep = self._duration - self._elapsed
      self._elapsed = self._duration
    # increase elapsed timer
    else:
      self._elapsed += timestep_

    return effectiveTimestep, None

############################################################################################
# DamagingAilment base
############################################################################################

class DamagingAilment(Duration):
  """docstring for DamagingAilment"""
  def __init__(self, name_, **kwargs_):
    super(DamagingAilment, self).__init__(name_ = name_, **kwargs_)
    self._types.append('damagingAilment')

    required = ['damage_', 'scalingTags_']
    toolbox.validateInput(self._name, required, **kwargs_)

    self._baseDamage = kwargs_['damage_']
    self._damage = self._baseDamage

    self._scalingTags = kwargs_['scalingTags_']


  def applyModifier(self, modifier_):
    super(DamagingAilment, self).applyModifier(modifier_)

    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # print(modifier_)
    # print(self._name)
    # print(self._damage)

    self._damage.imultiplyByFactor(modifier_.getDuration(self._name, 'effect'), shift_ = 1.)
    self._damage.imultiplyByFactor(modifier_.getIncreaseByTagList(self._scalingTags), shift_ = 1.)
    self._damage.imultiplyByFactor(modifier_.getMoreByTagList(self._scalingTags), shift_ = 0.)

    # print(self._damage)
    # print(self._duration)
    # print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

    pass

  def tick(self, timestep_):
    effectiveTimestep, _ = super(DamagingAilment, self).tick(timestep_)

    return effectiveTimestep, self._damage.multiplyByFactor(timestep_ / self._baseDuration)

############################################################################################
# Buff base
############################################################################################

class Buff(Duration):
  """docstring for Buff"""
  def __init__(self, name_, **kwargs_):
    super(Buff, self).__init__(name_ = name_, **kwargs_)

    self._types.append('buff')

    self._modifier = modifier.Modifier()

  def applyModifier(self, modifier_):
    super(Buff, self).applyModifier(modifier_)
    warnings.warn('buff.applyModifier() not implemented yet.')
    pass


  def getModifier(self):

    return self._modifier

############################################################################################
# ResistanceShred base
############################################################################################

class ResistanceShred(Duration):
  """docstring for Shred"""
  def __init__(self, name_, **kwargs_):
    super(ResistanceShred, self).__init__(name_ = name_, **kwargs_)

    required = ['shredElement_']
    toolbox.validateInput(self._name, required, **kwargs_)

    self._types.append('resistanceShred')

    self._shred = element.ElementContainer()

    self._shred.iassignByElement(kwargs_['shredElement_'], 0.05)

  def applyModifier(self, modifier_):
    super(ResistanceShred, self).applyModifier(modifier_)
    # todo: does poison shred scale with poison effect?!?!?!
    # would nee to scale self._shred values accordingly
    pass

  def getShred(self):

    return self._shred


############################################################################################
# Cooldown base
############################################################################################

class Cooldown(Duration):
  """docstring for Cooldown"""
  def __init__(self, name_, duration_):
    super(Cooldown, self).__init__(name_ = name_, duration_ = duration_, maxStacks_ = 1)

    self._types.append('cooldown')

############################################################################################
############################################################################################
# Duration object implementations
############################################################################################
############################################################################################

############################################################################################
# Buffs
############################################################################################

class RiveExecution(Buff):
  """docstring for RiveExecution"""
  def __init__(self):
    super(RiveExecution, self).__init__(name_ = 'riveExecution', duration_ = 2., maxStacks_ = 0)

    self._modifier.addIncrease('physical', 0.15)


############################################################################################
# DamagingAilments
############################################################################################

class Bleed(DamagingAilment):
  """docstring for Bleed"""
  def __init__(self):
    super(Bleed, self).__init__(name_ = 'bleed', duration_ = 4., damage_ = element.ElementContainer(physical = 53.), scalingTags_ =  ['generic', 'physical', 'physicalOverTime', 'overTime'], maxStacks_ = 0)

class Ignite(DamagingAilment):
  """docstring for Ignite"""
  def __init__(self):
    super(Ignite, self).__init__(name_ = 'ignite', duration_ = 3., damage_ = element.ElementContainer(fire = 33.), scalingTags_ =  ['generic', 'fire', 'fireOverTime', 'overTime'], maxStacks_ = 0)

class Poison(ResistanceShred, DamagingAilment):
  """docstring for Poison"""
  def __init__(self):
    super(Poison, self).__init__(name_ = 'poison', duration_ = 3., damage_ = element.ElementContainer(poison = 20.), scalingTags_ =  ['generic', 'poison', 'poisonOverTime', 'overTime'],  shredElement_ = 'poison', maxStacks_ = 0)

############################################################################################
# Shreds
############################################################################################

class PhysicalShred(ResistanceShred):
  """docstring for PhysicalShred"""
  def __init__(self):
    super(PhysicalShred, self).__init__(name_ = 'physicalShred', shredElement_ = 'physical', duration_ = 4, maxStacks_ = 20)

class PoisonShred(ResistanceShred):
  """docstring for PhysicalShred"""
  def __init__(self):
    super(PoisonShred, self).__init__(name_ = 'poisonShred', shredElement_ = 'poison', duration_ = 4, maxStacks_ = 20)

############################################################################################
############################################################################################
# Duration implementation information
############################################################################################
############################################################################################

import sys, inspect

# base classes
baseClasses = ['damagingAilment', 'resistanceShred', 'buff', 'duration', 'cooldown']

# collect all durations and to de-capitalize them
allClasses = [name[0].lower() + name[1:] for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass) if obj.__module__ is __name__]

# implemented class; allClasses.remove(baseClasses)
implementedClasses = [name for name in allClasses if name not in baseClasses] + ['cooldown']

def getBaseClasses():
  return baseClasses

def getAllClasses():
  return allClasses

def getImplementedClasses():
  return implementedClasses

############################################################################################
############################################################################################
# Duration object easy access
############################################################################################
############################################################################################

def getDefaultObjectByName(name_):
  if name_ in getImplementedClasses():
    # capitalize name of requested duration
    className = name_[0].upper() + name_[1:]
    return eval(className)()
  else:
    raise error.InvalidDuration(name_)
