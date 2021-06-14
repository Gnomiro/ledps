from data import supportedTags, supportedAttributes, supportedDurations, supportedDurationModifiers, supportedElementTypes, durationData, supportedProcs, supportedProcModifiers

from numpy import product as prod

import data

import errors

class Stats():

  def __init__(self):
    # todo: make getter for more/increase/... which combine relevant increases for skills/ailments
    # quest: keep scaling coefficients as list or single values? Can values be updated on the fly?
    # empty charcter sheet
    # increase modifiers
    self.increase = dict.fromkeys(supportedTags, 0.)
    # more modifiers
    self.more = dict.fromkeys(supportedTags, 1.)
    # penetration
    self.penetration = dict.fromkeys(supportedElementTypes, 0.)
    # attribute
    self.attribute = dict.fromkeys(supportedAttributes, 0.)
    # calculates duration dict based on cross product of duration and duration modifers
    # todo: rename later to durationModifiers
    self.duration = {d: {dm: 0. for dm in supportedDurationModifiers} for d in supportedDurations}

    self.proc = {p: {pm: 0. for pm in supportedProcModifiers} for p in supportedProcs}

    pass

  # create stat object based on active buffs in duration-container
  def fromBuffs(self, durations_):
    self.__init__()

    # count number of active buffs
    buffCount = durations_.countActiveByTypes('buff')

    # apply specific increases and more multipliers per stack into corresponding stat-slot
    # assuming that same more multipliers are still additive
    for bkey in buffCount.keys():
      # print(bkey)
      # print(buffCount[bkey])
      self.increase[durationData[bkey]['element']] += durationData[bkey]['increase'] * buffCount[bkey]
      self.more[durationData[bkey]['element']] *= (1. + durationData[bkey]['more'] * buffCount[bkey])
    pass

    return self

  def __str__(self):
    return 'increases:\n' + str(self.increase) + '\nmore:\n' + str(self.more) + '\npenetration:\n' + str(self.penetration) + '\nattribute:\n' + str(self.attribute) + '\nailments:\n' + str(self.duration)

  def getIncrease(self, name_):
    if name_ not in data.getSupportedTags():
      raise errors.InvalidTagError
    return self.increase.get(name_, 0.)

  def getMore(self, name_):
    if name_ not in data.getSupportedTags():
      raise errors.InvalidTagError
    return self.more.get(name_, 1.)

  def getPenetration(self, name_):
    if name_ not in data.getSupportedElementTypes():
      raise errors.InvalidElementError
    return self.penetration.get(name_, 0.)

    pass
  def getAttribute(self, name_):
    if name_ not in data.getSupportedAttributes():
      raise errors.InvalidAttributeError
    return self.attribute.get(name_, 0.)

  def getDurationModifier(self, name_, modifier_):
    if name_ not in data.getSupportedDurations():
      raise errors.InvalidDurationError
    if modifier_ not in data.getSupportedDurationModifiers():
      raise errors.InvalidDurationModifierError
    return self.duration.get(name_, 0.).get(modifier_, 0.)

  def getTriggerModifier(self, name_, modifier_):
    if name_ not in data.getSupportedTriggers():
      raise errors.InvalidTriggerError
    if modifier_ not in data.getSupportedTriggerModifiers():
      raise errors.InvalidTriggerModifierError
    return self.proc.get(name_, 0.).get(modifier_, 0.)

  def addIncrease(self, name_, value_):
    self.increase[name_] = self.getIncrease(name_) + value_
    pass

  def addMore(self, name_, value_):
    if value_ <= 1.:
      print('Warning: More modifiers should usually be greater than 1.')
    self.more[name_] = self.getMore(name_) * value_
    pass

  def addPenetration(self, name_, value_):
    self.penetration[name_] = self.getPenetration(name_) + value_
    pass

  def addAttribute(self, name_, value_):
    self.attribute[name_] = self.getAttribute(name_) + value_
    pass

  def addDurationModifier(self, name_, modifier_, value_):
    self.duration[name_][modifier_] = self.getDurationModifier(name_, modifier_) + value_
    pass

  def addTriggerModifier(self, name_, modifier_, value_):
    self.proc[name_][modifier_] = self.getTriggerModifier(name_, modifier_) + value_
    pass

  def setIncrease(self, name_, value_):
    if name_ not in data.getSupportedTags():
      raise errors.InvalidTagError
    self.increase[name_] = value_
    pass

  def setMore(self, name_, value_):
    if name_ not in data.getSupportedTags():
      raise errors.InvalidTagError
    if value_ <= 1.:
      print('Warning: More modifiers should usually be greater than 1.')
    self.more[name_] = value_
    pass

  def setPenetration(self, name_, value_):
    if name_ not in data.getSupportedElementTypes():
      raise errors.InvalidElementError
    self.penetration[name_] = value_
    pass

    pass
  def setAttribute(self, name_, value_):
    if name_ not in data.getSupportedAttributes():
      raise errors.InvalidAttributeError
    self.attribute[name_] = value_
    pass

  def setDurationModifier(self, name_, value_):
    if name_ not in data.getSupportedDurations():
      raise errors.InvalidDurationError
    if modifier_ not in data.getSupportedDurationModifiers():
      raise errors.InvalidDurationModifierError
    self.duration[name_][modifier_] = value_
    pass

  def setTriggerModifier(self, name_, value_):
    if name_ not in data.getSupportedTriggers():
      raise errors.InvalidTriggerError
    if modifier_ not in data.getSupportedTriggerModifiers():
      raise errors.InvalidTriggerModifierError
    self.proc[name_][modifier_] = value_
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
    self.proc['SentinelAxeThrower']['onHit'] += points * 0.08
    pass

  # palading tree talents
  def penance(self, points = 10):
    self.addDurationModifier('bleed', 'onMeleeHit', points * 0.2)
    self.addDurationModifier('bleed', 'onThrowHit', points * 0.2)
    pass

  def conviction(self, points = 8):
    self.addIncrease('physical', .04 * points)
    self.addPenetration('physical', .04 * points)
    self.addIncrease('fire', .02 * points)
    self.addPenetration('fire', .02 * points)
    pass

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
    self.addPenetration('physical', 0.05)
    pass

  def addSword(self):
    print("Sword")
    # implcits
    self.addMore('meleeAttackSpeed', 1.24)
    self.addIncrease('overTime', 0.48)
    # stats
    self.addIncrease('meleeAttackSpeed', 0.22)
    self.addIncrease('physical', 1.03)
    self.addDurationModifier('bleed', 'onHit', 0.49)
    pass

  def addAxe(self):
    print("Axe")
    # implicits
    self.addMore('meleeAttackSpeed', 1.05)
    self.addDurationModifier('bleed', 'onHit', 0.3)
    # stats
    self.addIncrease('meleeAttackSpeed', 0.22)
    self.addIncrease('physical', 1.03)
    self.addDurationModifier('bleed', 'onHit', 0.49)
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
    self.addIncrease('physical', 0.51)
    self.addIncrease('overTime', 0.19)
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