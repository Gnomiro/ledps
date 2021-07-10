import toolbox, error, element

import copy

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

  def isPermanent(self):
    return self._permanent

  def isActive(self):
    if self.isPermanent():
      return True
    else:
      return self._elapsed < self._duration

  def applyModifier(self, modifier_):
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

    required = ['damage_']
    toolbox.validateInput(self._name, required, **kwargs_)

    self._baseDamage = kwargs_['damage_']
    self._damage = self._baseDamage


  def applyModifier(self, modifier_):
    super(DamagingAilment, self).applyModifier(modifier_)
    print('Warning: damagingAilment.applyModifier() not implemented yet.')
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

    print('Warning: buff has no Modifier() object yet.')
    self._modifier = None

  def applyModifier(self, modifier_):
    super(Buff, self).applyModifier(modifier_)
    print('Warning: buff.applyModifier() not implemented yet.')
    pass


  def getModifier(self):

    print('Warning: buff.getModifier() not implemented yet.')

    return

############################################################################################
# Shred base
############################################################################################

class Shred(Duration):
  """docstring for Shred"""
  def __init__(self, name_, **kwargs_):
    super(Shred, self).__init__(name_ = name_, **kwargs_)

    required = ['shredElement_']
    toolbox.validateInput(self._name, required, **kwargs_)

    self._types.append('shred')
    self._shredElement = kwargs_['shredElement_']


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

############################################################################################
# DamagingAilments
############################################################################################

class Bleed(DamagingAilment):
  """docstring for Bleed"""
  def __init__(self):
    super(Bleed, self).__init__(name_ = 'bleed', duration_ = 4, damage_ = element.ElementContainer(physical = 53), maxStacks_ = 0)


class Poison(Shred, DamagingAilment):
  """docstring for Poison"""
  def __init__(self):
    super(Poison, self).__init__(name_ = 'poison', duration_ = 3, damage_ = element.ElementContainer(poison = 20), shredElement_ = 'physical', maxStacks_ = 0)

############################################################################################
# Shreds
############################################################################################

class PhysicalShred(Shred):
  """docstring for PhysicalShred"""
  def __init__(self):
    super(PhysicalShred, self).__init__(name_ = 'physicalShred', shredElement_ = 'physical', duration_ = 4, maxStacks_ = 20)

############################################################################################
############################################################################################
# Duration implementation information
############################################################################################
############################################################################################

import sys, inspect

# base duration types
baseDurations = ['cooldown', 'damagingAilment', 'shred', 'buff', 'duration']
# collect all durations and cast to de-capitalize
allDurations = [name[0].lower() + name[1:] for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass)if obj.__module__ is __name__]
#
implementedDurations = [name for name in allDurations if name not in baseDurations]

def getBaseDurations():
  return baseDurations

def getValidDurations():
  return allDurations

def getImplementedDurations():
  return implementedDurations

############################################################################################
############################################################################################
# Duration object easy access
############################################################################################
############################################################################################

def getDefaultDuration(name_):
  if name_ in getImplementedDurations():
    # capitalize name of requested duration
    className = name_[0].upper() + name_[1:]
    return eval(className + '()')
  else:
    raise error.InvalidDuration(name_)
