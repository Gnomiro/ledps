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
    pass

  def getName(self):
    return self._name

  def hasType(self, type_):
    return type_ in self._types

  def getTypes(self):
    return self._types

  def isApplicable(self):
    return self._maxStacks != 0

  def hasStackLimit(self):
    return self._maxStacks != -1

  def getMaxStacks(self):
    return self._maxStacks

  def setAppliedBy(self, skillName_, skillN_):
    self._appliedBy = (skillName_, skillN_)
    pass

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
    pass


  def applyModifier(self, modifier_):
    super(DamagingAilment, self).applyModifier(modifier_)

    self._damage.imultiplyByFactor(modifier_.getDuration(self._name, 'effect'), shift_ = 1.)
    self._damage.imultiplyByFactor(modifier_.getIncreaseByTagList(self._scalingTags), shift_ = 1.)
    self._damage.imultiplyByFactor(modifier_.getMoreByTagList(self._scalingTags), shift_ = 0.)

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
    pass

  def applyModifier(self, modifier_):
    super(Buff, self).applyModifier(modifier_)

    # use this alongside effect for aspect of the shark for now
    # print(modifier_.getDuration(self._name, 'effectMultiplier')) # effectMultiplier = 0 as default

    effect = modifier_.getDuration(self._name, 'effect')
    effectMultiplier = (1 if modifier_.getDuration(self._name, 'effectMultiplier') == 0 else modifier_.getDuration(self._name, 'effectMultiplier'))

    # only required if effect modifier are not 0
    if effect == 0  and effectMultiplier == 0:
      return

    for name, value in self._modifier.getIncreases().items():
      self._modifier.setIncrease(name, self._modifier.getIncrease(name) * (1. + effect) * (effectMultiplier))

    for name, value in self._modifier.getMores().items():
      self._modifier.setMore(name, self._modifier.getMore(name) * (1. + effect) * (effectMultiplier))

    for name, value in self._modifier.getPenetrations().items():
      self._modifier.setPenetration(name, self._modifier.getPenetration(name) * (1. + effect) * (effectMultiplier))

    # duration modification handled in base class; furthermore duration should not be scaled by effect

    for name, value in self._modifier.getAttributes().items():
      warnings.warn('buff.applyModifier(): Effect does not scale attributes from buffs.')
      pass

    for name in self._modifier.getDurations().keys():
      for modifier, value in self._modifier.getDurations()[name].items():
        self._modifier.setDuration(name, modifier, self._modifier.getDuration(name, modifier) * (1. + effect) * (effectMultiplier))

    for name in self._modifier.getTriggers().keys():
      warnings.warn('buff.applyModifier(): Effect does not trigger chances from buffs.')
      pass

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
    pass

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
    pass

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
    super(RiveExecution, self).__init__(name_ = 'riveExecution', duration_ = 2., maxStacks_ = -1)

    self._modifier.addIncrease('physical', 0.15)
    pass

class AspectOfTheShark(Buff):
  """docstring for AspectOfTheShark"""
  def __init__(self):
    super(AspectOfTheShark, self).__init__(name_ = 'aspectOfTheShark', duration_ = 3., maxStacks_ = 1)

    self._modifier.addIncrease('melee', 0.5)
    self._modifier.addIncrease('meleeAttackSpeed', 0.1)
    pass

class AspectOfTheBoar(Buff):
  """docstring for AspectOfTheBoar"""
  def __init__(self):
    super(AspectOfTheBoar, self).__init__(name_ = 'aspectOfTheBoar', duration_ = 0., maxStacks_ = 1)

    # aspect of the boar has a default duration of 0 and provides nothing without talents

    pass

class AspectOfTheViper(Buff):
  """docstring for AspectOfTheViper"""
  def __init__(self):
    super(AspectOfTheViper, self).__init__(name_ = 'aspectOfTheViper', duration_ = 3., maxStacks_ = 1)

    self._modifier.addIncrease('damageOverTime', 1.)
    self._modifier.addDuration('poison', 'onHit', 1.)
    pass

# Swipe aspect of the panther stackable part
class SwipeAspectOfThePantherStackable(Buff):
  """docstring for SwipeAspectOfThePantherStackable"""
  def __init__(self):
    super(SwipeAspectOfThePantherStackable, self).__init__(name_ = 'swipeAspectOfThePantherStackable', duration_ = 4., maxStacks_ = 0)

    pass

# Swipe aspect of the panther not stackable part
class SwipeAspectOfThePantherNotStackable(Buff):
  """docstring for SwipeAspectOfThePantherNotStackable"""
  def __init__(self):
    super(SwipeAspectOfThePantherNotStackable, self).__init__(name_ = 'swipeAspectOfThePantherNotStackable', duration_ = 4., maxStacks_ = 1)

    pass

class SerpentStrikeScorpionStrikes(Buff):
  """docstring for SerpentStrikeScorpionStrikes"""
  def __init__(self):
    super(SerpentStrikeScorpionStrikes, self).__init__(name_ = 'serpentStrikeScorpionStrikes', duration_ = 4., maxStacks_ = -1)

    pass

class SerpentStrikeChronoStrike(Buff):
  """docstring for SerpentStrikeChronoStrike"""
  def __init__(self):
    super(SerpentStrikeChronoStrike, self).__init__(name_ = 'serpentStrikeChronoStrike', duration_ = 4., maxStacks_ = -1)

    pass

############################################################################################
# DamagingAilments
############################################################################################

class Bleed(DamagingAilment):
  """docstring for Bleed"""
  def __init__(self):
    super(Bleed, self).__init__(name_ = 'bleed', duration_ = 4., damage_ = element.ElementContainer(physical = 53.), scalingTags_ =  ['generic', 'physical', 'physicalOverTime', 'overTime'], maxStacks_ = -1)

class Ignite(DamagingAilment):
  """docstring for Ignite"""
  def __init__(self):
    super(Ignite, self).__init__(name_ = 'ignite', duration_ = 3., damage_ = element.ElementContainer(fire = 33.), scalingTags_ =  ['generic', 'fire', 'fireOverTime', 'overTime'], maxStacks_ = -1)

class Poison(ResistanceShred, DamagingAilment):
  """docstring for Poison"""
  def __init__(self):
    super(Poison, self).__init__(name_ = 'poison', duration_ = 3., damage_ = element.ElementContainer(poison = 20.), scalingTags_ =  ['generic', 'poison', 'poisonOverTime', 'overTime'],  shredElement_ = 'poison', maxStacks_ = -1)

class Plague(DamagingAilment):
  """docstring for Plague"""
  def __init__(self):
    super(Plague, self).__init__(name_ = 'plague', duration_ = 4., damage_ = element.ElementContainer(poison = 90.), scalingTags_ =  ['generic', 'poison', 'poisonOverTime', 'overTime'],  shredElement_ = 'poison', maxStacks_ = 1)

class BlindingPoison(DamagingAilment):
  """docstring for BlindingPoison"""
  def __init__(self):
    super(BlindingPoison, self).__init__(name_ = 'blindingPoison', duration_ = 4., damage_ = element.ElementContainer(poison = 30.), scalingTags_ =  ['generic', 'poison', 'poisonOverTime', 'overTime'],  shredElement_ = 'poison', maxStacks_ = 1)

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
