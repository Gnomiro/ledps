from numpy import product as prod

import data

import errors

class Stats():

  # initialize empty stat sheet
  def __init__(self):

    # increase modifiers
    self._increase = {}
    # more modifiers
    self._more = {}
    # penetration
    self._penetration = {}
    # attribute
    self._attribute = {}
    # durationModifiers
    self._durationModifier = {}
    # triggerModifiers
    self._triggerModifier = {}

    pass

  # create stat object based on active buffs in duration-container
  # gearAndSkillStats_: gear and skills can provide increased buff effects
  def fromBuffs(self, durations_, gearAndSkillStats_):
    self.__init__()

    # count number of active buffs
    buffCount = durations_.countActiveByTypes('buff', 'skillProvidedBuff')

    # apply specific increases and more multipliers per stack into corresponding stat-slot
    for name, stacks in buffCount.items():
      # print(name)

      # get buff data and iterate over provided stat-types (increase, more, duration, ...) and associated buffs-types (physical, attackSpeed, ...)
      for statType, buffTypes in data.getDurationData()[name]['effect'].items():

        # print(statType)
        # iterate over buffTypes to get individual stat-buffs and values
        for buffType, value in buffTypes.items():
          # print(buffType)
          # print(value)

          # todo: probably change loop style to have if/else-statement at outer loop
          # todo: add support for more types
          if statType == 'increase':
            self.addIncrease(buffType, value * stacks * (1. + gearAndSkillStats_.getDurationModifier(name, 'effect')))
            # print('name : {}, statTye : {}, buffType : {}, v : {}, stacks: {}, effect : {}'.format(name, statType, buffType, value, stacks, gearAndSkillStats_.getDurationModifier(name, 'effect')))
          elif statType == 'more':
            self.addMore(buffType, value * stacks * (1. + gearAndSkillStats_.getDurationModifier(name, 'effect')))
            # print('name : {}, statTye : {}, buffType : {}, v : {}, stacks: {}, effect : {}'.format(name, statType, buffType, value, stacks, gearAndSkillStats_.getDurationModifier(name, 'effect')))
          elif statType == 'duration':
            for dm, v in value.items():
              # print(dm)
              # print(v)
              # todo: is this correct? scaling buff effects
              # print('name : {}, statTye : {}, buffType : {}, dm : {}, v : {}, stacks: {}, effect : {}'.format(name, statType, buffType, dm, v, stacks, gearAndSkillStats_.getDurationModifier(name, 'effect')))
              self.addDurationModifier(buffType, dm, v * stacks * (1. + gearAndSkillStats_.getDurationModifier(name, 'effect')))
          else:
            print('Warning: Allocation of buff-type not supported yet')
    pass

    return self

  # add other_ to self; operator +=
  def __iadd__(self, other_):
    for name, value in other_._increase.items():
      self.addIncrease(name, value)
    for name, value in other_._more.items():
      self.addMore(name, value)
    for name, value in other_._penetration.items():
      self.addPenetration(name, value)
    for name, value in other_._attribute.items():
      self.addAttribute(name, value)
    for name in other_._durationModifier.keys():
      for modifier, value in other_._durationModifier[name].items():
        self.addDurationModifier(name, modifier, value)
    for name in other_._triggerModifier.keys():
      for modifier, value in other_._triggerModifier[name].items():
        self.addTriggerModifier(name, modifier, value)
    return self

  # add two stats opjects and return new one containing both information
  def __add__(self, other_):
    total = Stats()

    total += self
    total += other_

    return total

  def __str__(self):
    return 'increases:\n' + str(self._increase) + '\nmore:\n' + str(self._more) + '\npenetration:\n' + str(self._penetration) + '\nattribute:\n' + str(self._attribute) + '\ndurationModifier:\n' + str(self._durationModifier) + '\ntriggerModifier:\n' + str(self._triggerModifier)

  def getPenetrations(self):
    return self._penetration

  def getDurationModifiers(self):
    return self._durationModifier

  def getIncrease(self, name_):
    if name_ not in data.getSupportedTags():
      raise errors.InvalidTagError
    return self._increase.get(name_, 0.)

  def getMore(self, name_):
    if name_ not in data.getSupportedTags():
      raise errors.InvalidTagError
    return self._more.get(name_, 1.)

  def getPenetration(self, name_):
    if name_ not in data.getSupportedElementTypes():
      raise errors.InvalidElementError
    return self._penetration.get(name_, 0.)

    pass
  def getAttribute(self, name_):
    if name_ not in data.getSupportedAttributes():
      raise errors.InvalidAttributeError
    return self._attribute.get(name_, 0.)

  def getDurationModifier(self, name_, modifier_):
    if name_ not in data.getSupportedDurations():
      raise errors.InvalidDurationError
    if modifier_ not in data.getSupportedDurationModifiers():
      raise errors.InvalidDurationModifierError
    return (self._durationModifier.get(name_, 0.) if name_ not in self._durationModifier.keys() else self._durationModifier.get(name_).get(modifier_, 0.))

  def getTriggerModifier(self, name_, modifier_):
    if name_ not in data.getSupportedTriggers():
      raise errors.InvalidTriggerError
    if modifier_ not in data.getSupportedTriggerModifiers():
      raise errors.InvalidTriggerModifierError
    return (self._triggerModifier.get(name_, 0.) if name_ not in self._triggerModifier.keys() else self._triggerModifier.get(name_).get(modifier_, 0.))

  def addIncrease(self, name_, value_):
    self._increase[name_] = self.getIncrease(name_) + value_
    pass

  def addMore(self, name_, value_):
    # if value_ < 1.:
    #   print('Warning: More modifiers should usually be greater than 1.')
    self._more[name_] = self.getMore(name_) * value_
    pass

  def addPenetration(self, name_, value_):
    self._penetration[name_] = self.getPenetration(name_) + value_
    pass

  def addAttribute(self, name_, value_):
    self._attribute[name_] = self.getAttribute(name_) + value_
    pass

  def addDurationModifier(self, name_, modifier_, value_):
    if name_ not in self._durationModifier.keys():
      self._durationModifier[name_] = {}
    self._durationModifier[name_][modifier_] = self.getDurationModifier(name_, modifier_) + value_
    pass

  def addTriggerModifier(self, name_, modifier_, value_):
    if name_ not in self._triggerModifier.keys():
      self._triggerModifier[name_] = {}
    self._triggerModifier[name_][modifier_] = self.getTriggerModifier(name_, modifier_) + value_
    pass

  def setIncrease(self, name_, value_):
    if name_ not in data.getSupportedTags():
      raise errors.InvalidTagError
    self._increase[name_] = value_
    pass

  def setMore(self, name_, value_):
    if name_ not in data.getSupportedTags():
      raise errors.InvalidTagError
    if value_ <= 1.:
      print('Warning: More modifiers should usually be greater than 1.')
    self._more[name_] = value_
    pass

  def setPenetration(self, name_, value_):
    if name_ not in data.getSupportedElementTypes():
      raise errors.InvalidElementError
    self._penetration[name_] = value_
    pass

    pass
  def setAttribute(self, name_, value_):
    if name_ not in data.getSupportedAttributes():
      raise errors.InvalidAttributeError
    self._attribute[name_] = value_
    pass

  def setDurationModifier(self, name_, value_):
    if name_ not in data.getSupportedDurations():
      raise errors.InvalidDurationError
    if modifier_ not in data.getSupportedDurationModifiers():
      raise errors.InvalidDurationModifierError
    if name_ not in self._durationModifier.keys():
      self._durationModifier[name_] = {}
    self._durationModifier[name_][modifier_] = value_
    pass

  def setTriggerModifier(self, name_, value_):
    if name_ not in data.getSupportedTriggers():
      raise errors.InvalidTriggerError
    if modifier_ not in data.getSupportedTriggerModifiers():
      raise errors.InvalidTriggerModifierError
    if name_ not in self._triggerModifier.keys():
      self._triggerModifier[name_] = {}
    self._triggerModifier[name_][modifier_] = value_
    pass

  # sums up all relevant increases as requested by 'tags_' list
  def getIncreaseByTagList(self, tags_):
    return sum([self.getIncrease(t) for t in tags_])

  # sums up all relevant increases as requested by 'tags_' list
  def getMoreByTagList(self, tags_):
    return prod([(self.getMore(t)) for t in tags_])

  # class function
  def paladin(self):
    self.addIncrease('physical', 1.)
    self.addIncrease('fire', 1.)
    self.addAttribute('strength', 2)
    pass

  # sentinel tree talents
  def juggernaut(self, points = 8):
    self.addAttribute('strength', points)
    pass

  def blademaster(self, points = 5):
    self.addIncrease('meleeAttackSpeed', 0.06 * points)
    pass

  def axeThrower(self, points = 5):
    self.addTriggerModifier('SentinelAxeThrower', 'onHit', points * 0.08)
    pass

  # palading tree talents
  def penance(self, points = 10):
    self.addDurationModifier('bleed', 'onMeleeHit', points * 0.2)
    self.addDurationModifier('bleed', 'onThrowHit', points * 0.2)
    pass

  def conviction(self, points = 8):
    self.addIncrease('physical', .04 * points)
    self.addPenetration('physical', .02 * points)
    self.addIncrease('fire', .04 * points)
    self.addPenetration('fire', .02 * points)
    pass

  def divineBolt(self, points = 1):
    self.addTriggerModifier('DivineBolt', 'onMeleeHit', 0.2)

  def sharedDivinity(self, points = 5):
    # does not shotgun the same target!
    # data.supportedTriggerData['DivineBolt']['onTriggerExecutions'] += 1 * points
    data.supportedTriggerData['DivineBolt']['onHitEffectiveness'] *= (1. - 0.1 * points)

  def redemption(self, points = 7, recentlyHit = False):
    self.addDurationModifier('bleed', 'effect', 0.07 * points)
    if recentlyHit:
      self.addIncrease('generic', 0.07 * points)
    pass

  def reverenceOfDuality(self, points = 12):
    self.addIncrease('generic', 0.02 * points)
    pass

  # paladin skills with talents
  # manage active part later as buff
  def holyAura(self, callToArms = 0, fanaticism = 0, active = False):
    factor = (2. if active else 1.) # effects doubled if aura active
    self.addIncrease('generic', 0.3 * factor)
    self.addIncrease('physical', 0.1 * callToArms * factor)
    self.addIncrease('meleeAttackSpeed', 0.04 * fanaticism * factor)
    pass

  def sigilsOfHope(self, tetragram = False, empoweringSigils = 5, numberOfSigils = None):
    # if numberOfSigils is not proved maximum number is assumed
    if numberOfSigils == None:
      if tetragram:
        numberOfSigils = 4
      else:
        numberOfSigils = 3
    self.addIncrease('generic', 0.06 * empoweringSigils * numberOfSigils)
    pass

  # gear add functions
  def addHelmet(self):
    self.addIncrease('physical', 0.36)
    self.addDurationModifier('bleed', 'effect', 0.34)
    self.addDurationModifier('bleed', 'duration', 0.18)
    pass

  def addAmulet(self):
    self.addIncrease('physical', 0.99)
    self.addPenetration('physical', 0.08)
    pass

  def addSword(self):
    print("Sword")
    # implcits
    self.addMore('meleeAttackSpeed', 1.24)
    self.addIncrease('overTime', 0.43)
    # stats
    self.addIncrease('meleeAttackSpeed', 0.22)
    self.addIncrease('physical', 0.68)
    self.addDurationModifier('bleed', 'onHit', 1.05)
    pass

  def addAxe(self):
    print("Axe")
    # implcits
    self.addMore('meleeAttackSpeed', 1.05)
    self.addDurationModifier('bleed', 'onHit', 0.3)
    # stats
    self.addIncrease('meleeAttackSpeed', 0.22)
    self.addIncrease('physical', 0.68)
    self.addDurationModifier('bleed', 'onHit', 1.05)
    pass

  def addUndisputed(self):
    print("Undisputed")
    # implicits
    self.addMore('meleeAttackSpeed', 1.05)
    self.addDurationModifier('bleed', 'onHit', 0.3)
    # stats
    self.addIncrease('meleeAttackSpeed', 0.27)
    self.addDurationModifier('undisputed', 'onMeleeHit', 1.0)
    pass

  def addChest(self):
    self.addIncrease('physical', 0.58)
    self.addDurationModifier('bleed', 'effect', 0.67)
    self.addDurationModifier('bleed', 'duration', 0.29)
    pass

  def addShield(self):
      pass

  def addRing1(self):
    self.addIncrease('physical', 0.53)
    self.addIncrease('overTime', 0.33)
    pass

  def addBelt(self):
    self.addIncrease('physical', 0.56)
    pass

  def addRing2(self):
    self.addIncrease('physical', 0.59)
    self.addAttribute('strength', 2)
    pass

  def addGloves(self):
    self.addIncrease('meleeAttackSpeed', 0.39)
    pass

  def addBoots(self):
    self.addDurationModifier('doom', 'onHit', 0.25)
    self.addIncrease('overTime', 1.17)
    pass

  def addRelic(self):
    self.addDurationModifier('bleed', 'onHit', 0.25)
    self.addDurationModifier('bleed', 'duration', 0.48)
    pass

  def addIdol(self):
    self.addDurationModifier('bleed', 'duration', 0.2)
    self.addIncrease('physicalOverTime', 0.52)
    pass