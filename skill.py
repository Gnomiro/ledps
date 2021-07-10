import random, numpy
random.seed()

from itertools import cycle
from math import floor

import element, modifier, durationContainer, collection, character, error

# todo: change all catalogue to collection

verbosity = 0

class Default:

  def __init__(self, attacktimes_= None, attackdelays_ = None, pattern_ = None):
    self._skillName = 'default'

    if attacktimes_ == None:
      self._attacktimes = list([0.68182])
    else:
      self._attacktimes = attacktimes_
    if attackdelays_ == None:
      self._attackdelays = list([0])
    else:
      self._attackdelays = attackdelays_

    self._nAttacks = len(self._attacktimes)
    self._pattern = pattern_
    if pattern_ == None:
      self._pattern = range(len(attacktimes_))

    self._skillCooldown = 0
    self._talents = {}

    self._collection = collection.Collection()

    self._durationContainer = durationContainer.DurationContainer(self._collection)

    self._canTrigger = True

    self._prepared = False
    pass

  def setCollection(self, collection_):
    self._prepared = False
    self._collection = collection_
    pass

  def setDurationContainer(self, durationContainer_):
    self._prepared = False
    self._durationContainer = durationContainer_
    pass

  def setTalent(self, **talents_):
    for key, value in talents_.items():
      # cast input: uncapitalize key, cast value to integer
      key, value = key[0].lower() + key[1:], int(value)
      if key in self._talents.keys():
        if value > self._talents[key][1] or value < 0:
          print('Warning: Value \'{}\' not supported for talent \'{}\' of \'{}\'. Set to \'{}\' instead.'.format(value, key,  self._skillName, self._talents[key][1]))
          self._talents[key][0] = self._talents[key][1]
        else:
          self._talents[key][0] = value
      else:
        print('Warning: Talent with name \'{}\' is not available for \'{}\'. Skipped.'.format(key, self._skillName))
        continue
      if verbosity >= 1:
        print('{}: {}'.format(key, self._talents[key][0]))
      self._prepared = False
    pass

  def prepare(self):
    if not self._prepared:
      self._attributeModifier = modifier.Modifier()
      self._localSkillModifier = [modifier.Modifier() for i in range(self._nAttacks)]
      self.prepareSkill()
      self._patternCycle = cycle(self._pattern)
      self._n = next(self._patternCycle)
      self._prepared = True
      pass

  def prepareSkill(self):
    pass

  def attack(self, canTriggerOverride_ = None):

    self.prepare()

    allModifier = modifier.fromBuff(self._durationContainer)
    allModifier.iaddMultiple(self._collection.getPersistentModifier(), self._localSkillModifier[self._n], self._attributeModifier)

    damage = element.ElementContainer()

    if self._durationContainer.addCooldown(self._skillName, self._skillCooldown):

      skillDamage = self.skillHit(allModifier)
      damage += skillDamage

      resistances = element.ElementContainer(default_ = 0.0)
      penetration = element.ElementContainer(default_ = 0.0, **allModifier.getPenetrations())
      shred = element.fromShred(self._durationContainer)
      resistances -= shred
      resistances.setUpperLimit(0.75)
      penetration -= resistances
      damage.imultiply(penetration, shift_ = 1.0)

      self.skillEffect(allModifier)
      allModifier = modifier.fromBuff(self._durationContainer)
      allModifier.iaddMultiple(self._collection.getPersistentModifier(), self._localSkillModifier[self._n], self._attributeModifier)

      self.applyOnHit(allModifier)
      allModifier = modifier.fromBuff(self._durationContainer)
      allModifier.iaddMultiple(self._collection.getPersistentModifier(), self._localSkillModifier[self._n], self._attributeModifier)

      if (canTriggerOverride_ if canTriggerOverride_ is not None else self._canTrigger):
        triggerDamage = self.onHitTrigger(allModifier)
        allModifier = modifier.fromBuff(self._durationContainer)
        allModifier.iaddMultiple(self._collection.getPersistentModifier(), self._localSkillModifier[self._n], self._attributeModifier)
        damage += triggerDamage # penetration already applied in skill's own attack routine

      self._n = next(self._patternCycle)

    else:
      if verbosity >= 1:
        print(self._skillName + ' is still on cooldown')

    return (damage, self.getAttacktime(allModifier))

  def skillHit(self, modifier_):
    damage = element.ElementContainer()
    return damage

  def getOnHitChance(self, name_, modifier_):
    chance = modifier_.getDuration(name_, 'onHit')
    return chance

  def applyOnHit(self, modifier_):
    for name, info in modifier_.getDurations().items():
      chance = self.getOnHitChance(name, modifier_)
      if chance != 0:
        applications = floor(chance)
        if applications != chance:
          if random.random() <= chance - applications:
            applications += 1
        for i in range(applications):
          self._durationContainer.add(name, modifier_ = modifier_, skillName_= self._skillName , skillN_ = self._n)
    pass

  def skillEffect(self, modifier_):
    pass

  def getTriggerChance(self, trigger_, modifier_):
    chance = modifier_.getTrigger(trigger_, 'onHit')
    return chance

  def onHitTrigger(self, modifier_):
    damage = element.ElementContainer()
    for trigger, info in modifier_.getTriggers().items():
      chance = self.getTriggerChance(trigger, modifier_)
      if chance != 0:
        skill = self._catalogue.getSkillOnTheFlytriggerself._catalogueself._durationContainerself._persistentModifier
        applications = floor(chance)
        if applications != chance:
          if random.random() <= chance - applications:
            applications += 1
        for i in range(applications):
          triggerDamage, _ = self._collection.getSkillOnTheFly(self._durationContainer).attack(canTriggerOverride_ = False)
          damage += triggerDamage
      return damage

  def getSkillModifier(self, n_=0):
    self.prepare()
    return self._localSkillModifier[n_]

  def getAttacktime(self, modifier_):
    self.prepare()
    return self._attackdelays[self._n] + self._attacktimes[self._n] / (1.0 + modifier_.getIncrease('meleeAttackSpeed')) / modifier_.getMore('meleeAttackSpeed')


class Melee(Default):

  def __init__(self, attacktimes_= [0.68182], attackdelays_ = [0], pattern_ = None):
    super().__init__(attacktimes_ = attacktimes_, attackdelays_ = attackdelays_, pattern_ = pattern_)

    self._skillName = 'melee'
    pass

  def getOnHitChance(self, name_, modifier_):
    chance = modifier_.getDuration(name_, 'onHit') + modifier_.getDuration(name_, 'onMeleeHit')
    return chance

  def getTriggerChance(self, trigger_, modifier_):
    chance = modifier_.getTrigger(trigger_, 'onHit') + modifier_.getTrigger(trigger_, 'onMeleeHit')
    return chance


class Spell(Default):

  def __init__(self, attacktimes_ = [0.68182], attackdelays_ = [0], pattern_ = None):
    super().__init__(attacktimes_ = attacktimes_, attackdelays_ = attackdelays_, pattern_ = pattern_)

    self._skillName = 'spell'
    pass

  def getOnHitChance(self, name_, modifier_):
    chance = modifier_.getDuration(name_, 'onHit') + modifier_.getDuration(name_, 'onSpellHit')
    return chance

  def getTriggerChance(self, trigger_, modifier_):
    chance = modifier_.getTrigger(trigger_, 'onHit') + modifier_.getTrigger(trigger_, 'onSpellHit')
    return chance


class Throw(Default):

  def __init__(self, attacktimes_ = [0.68182], attackdelays_ = [0], pattern_ = None):
    super().__init__(attacktimes_ = attacktimes_, attackdelays_ = attackdelays_, pattern_ = pattern_)

    self._skillName = 'throw'
    pass

  def getOnHitChance(self, name_, modifier_):
    chance = modifier_.getDuration(name_, 'onHit') + modifier_.getDuration(name_, 'onThrowHit')
    return chance

  def getTriggerChance(self, trigger_, modifier_):
    chance = modifier_.getTrigger(trigger_, 'onHit') + modifier_.getTrigger(trigger_, 'onThrowHit')
    return chance


class Rive(Melee):

  def __init__(self):
    super().__init__(attacktimes_ = [0.511365, 0.511365, 0.477274], attackdelays_ = [0.02, 0.02, 0.005], pattern_ = [0, 1, 2])

    self._skillName = 'rive'

    self._talents = {'cadence': [0, 1],
                     'flurry': [0, 5],
                     'sever': [0, 3],
                     'twistingFangs': [0, 3],
                     'execution': [0, 1],
                     'indomitable': [0, 1],
                     'ironReach': [0, 4],
                     'tripleThreat': [0, 1]}
    pass

  def prepareSkill(self):

    self._localSkillModifier[0].addIncrease('meleeAttackSpeed', 0.08 * self._talents['flurry'][0])
    self._localSkillModifier[1].addIncrease('meleeAttackSpeed', 0.08 * self._talents['flurry'][0])

    self._localSkillModifier[0].addDuration('ignite', 'onHit', 0.5 * self._talents['sever'][0])

    self._localSkillModifier[1].addDuration('ignite', 'onHit', 0.5 * self._talents['twistingFangs'][0])

    self._localSkillModifier[1].addMore('generic', 1.0 + 0.25 * self._talents['ironReach'][0])

    self._localSkillModifier[2].addMore('generic', 1.0 + 0.5 * self._talents['tripleThreat'][0])

    if self._talents['cadence'][0] == 1:
      self._pattern = [0, 1, 0, 1, 2]

    self._localSkillModifier[0].addTrigger('RiveIndomitable', 'onHit', 1.0 * self._talents['indomitable'][0])

    self._attributeModifier.addIncrease('generic', 0.04 * self._collection.getPersistentModifier().getAttribute('strength'))
    pass

  def skillHit(self, modifier_):
    damage = element.ElementContainer()
    return damage

  def skillEffect(self, modifier_):
    if self._talents['execution'][0] == 1 and self._n == 2:
      nIgnites = self._durationContainer.countActiveByNames('ignite')['ignite']
      self._durationContainer._durations['ignite'] = list([])
      for i in range(nIgnites):
        self._durationContainer.add('riveExecution', modifier_)
    pass



class ManifestStrike(Melee):

  def __init__(self):
    super().__init__(attacktimes_ = [0], attackdelays_ = [0], pattern_ = None)
    self._skillName = 'manifestStrike'

    # generally this skill can trigger, if triggered this tag is overriden in base class to disable chaining triggers
    # self._canTrigger = False
    pass

  def prepareSkill(self):
    self._attributeModifier.addIncrease('generic', 0.04 * self._collection.getPersistentModifier().getAttribute('strength'))
    self._attributeModifier.addIncrease('generic', 0.04 * self._collection.getPersistentModifier().getAttribute('attunement'))
    pass

  def skillHit(self, modifier_):
    damage = element.ElementContainer()
    return damage


class SentinelAxeThrower(Throw):

  def __init__(self):
    super().__init__(attacktimes_ = [0], attackdelays_ = [0], pattern_ = None)
    self._skillName = 'sentinelAxeThrower'

    self._skillCooldown = 1

    # generally this skill can trigger, if triggered this tag is overriden in base class to disable chaining triggers
    # self._canTrigger = False
    pass

  def prepareSkill(self):
    self._attributeModifier.addIncrease('generic', 0.04 * self._collection.getPersistentModifier().getAttribute('strength'))
    self._attributeModifier.addIncrease('generic', 0.04 * self._collection.getPersistentModifier().getAttribute('dexterity'))
    pass

  def skillHit(self, modifier_):
    damage = element.ElementContainer()
    return damage


class RiveIndomitable(Spell):

  def __init__(self):
    super().__init__(attacktimes_ = [0], attackdelays_ = [0], pattern_ = None)
    self._skillName = 'riveIndomitable'

    # generally this skill can trigger, if triggered this tag is overriden in base class to disable chaining triggers
    # self._canTrigger = False
    pass

  def prepareSkill(self):
    self._attributeModifier.addIncrease('generic', 0.04 * self._collection.getPersistentModifier().getAttribute('strength'))
    pass

  def skillHit(self, modifier_):
    damage = element.ElementContainer()
    return damage


class DivineBolt(Spell):

  def __init__(self):
    super().__init__(attacktimes_ = [0], attackdelays_ = [0], pattern_ = None)
    self._skillName = 'divineBolt'

    # generally this skill can trigger, if triggered this tag is overriden in base class to disable chaining triggers
    # self._canTrigger = False
    pass

  def prepareSkill(self):
    self._attributeModifier.addIncrease('generic', 0.04 * self._collection.getPersistentModifier().getAttribute('attunement'))
    pass

  def skillHit(self, modifier_):
    damage = element.ElementContainer()
    return damage


def getDefaultObjectByName(name_):
  if name_ in getImplementedDurations():
    # capitalize name of requested duration
    skillName = name_[0].upper() + name_[1:]
    return eval(skillName)()
  else:
    raise error.UnsupportedSkill(name_)


############################################################################################
############################################################################################
# Skill implementation information
############################################################################################
############################################################################################

import sys, inspect

# base classes
baseClasses = ['default']

# collect all durations and to de-capitalize them
allClasses = [name[0].lower() + name[1:] for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass) if obj.__module__ is __name__]

# implemented class; allClasses.remove(baseClasses)
implementedClasses = [name for name in allClasses if name not in baseClasses]

def getBaseClasses():
  return baseClasses

def getAllClasses():
  return allClasses

def getImplementedClasses():
  return implementedClasses

############################################################################################
############################################################################################
# Skill object easy access
############################################################################################
############################################################################################

def getDefaultObjectByName(name_):
  if name_ in getImplementedClasses():
    # capitalize name of requested duration
    className = name_[0].upper() + name_[1:]
    return eval(className)()
  else:
    raise error.UnsupportedSkill(name_)