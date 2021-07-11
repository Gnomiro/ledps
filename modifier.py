from numpy import product as prod, sum

############################################################################################
############################################################################################
# Modifier collection class
############################################################################################
############################################################################################

class Modifier():
  """docstring for Modifier"""

    # todo: refactor
    # notes
    # more = [generic, hit, spell, ...] x ElementContainer()
    # increase = [generic, hit, spell, ...] x ElementContainer()
    # flat = ElementContainer() + adaptive

  def __init__(self):
    self._increase = {}
    self._more = {}
    self._penetration = {}
    self._attribute = {}
    self._duration = {}
    self._trigger = {}
    pass

  def __iadd__(self, other_):
    for name, value in other_._increase.items():
      self.addIncrease(name, value)

    for name, value in other_._more.items():
      self.addMore(name, value)

    for name, value in other_._penetration.items():
      self.addPenetration(name, value)

    for name, value in other_._attribute.items():
      self.addAttribute(name, value)

    for name in other_._duration.keys():
      for modifier, value in other_._duration[name].items():
        self.addDuration(name, modifier, value)

    for name in other_._trigger.keys():
      for modifier, value in other_._trigger[name].items():
        self.addTrigger(name, modifier, value)

    return self

  def __add__(self, other_):
    total = Modifier()
    total += self
    total += other_
    return total

  def iaddMultiple(self, *other_):
    for other in other_:
      self += other
    return self

  def __str__(self):
    return 'increases:\n' + str(self._increase) + '\nmore:\n' + str(self._more) + '\npenetration:\n' + str(self._penetration) + '\nattribute:\n' + str(self._attribute) + '\nduration:\n' + str(self._duration) + '\ntrigger:\n' + str(self._trigger)

  def getIncreases(self):
    return self._increase

  def getMores(self):
    return self._more

  def getPenetrations(self):
    return self._penetration

  def getAttributes(self):
    return self._attribute

  def getDurations(self):
    return self._duration

  def getTriggers(self):
    return self._trigger

  def getIncrease(self, name_):
    return self._increase.get(name_, 0.0)

  def getMore(self, name_):
    return self._more.get(name_, 1.0)

  def getPenetration(self, name_):
    return self._penetration.get(name_, 0.0)

  def getAttribute(self, name_):
    return self._attribute.get(name_, 0.0)

  def getDuration(self, name_, modifier_):
    if name_ not in self._duration.keys():
      return self._duration.get(name_, 0.0)
    return self._duration.get(name_).get(modifier_, 0.0)

  def getTrigger(self, name_, modifier_):
    if name_ not in self._trigger.keys():
      return self._trigger.get(name_, 0.0)
    return self._trigger.get(name_).get(modifier_, 0.0)

  def addIncrease(self, name_, value_):
    self._increase[name_] = self.getIncrease(name_) + value_

  def addMore(self, name_, value_):
    self._more[name_] = self.getMore(name_) * value_

  def addPenetration(self, name_, value_):
    self._penetration[name_] = self.getPenetration(name_) + value_

  def addAttribute(self, name_, value_):
    self._attribute[name_] = self.getAttribute(name_) + value_

  def addDuration(self, name_, modifier_, value_):
    if name_ not in self._duration.keys():
      self._duration[name_] = {}
    self._duration[name_][modifier_] = self.getDuration(name_, modifier_) + value_

  def addTrigger(self, name_, modifier_, value_):
    if name_ not in self._trigger.keys():
      self._trigger[name_] = {}
    self._trigger[name_][modifier_] = self.getTrigger(name_, modifier_) + value_

  def setIncrease(self, name_, value_):
    self._increase[name_] = value_

  def setMore(self, name_, value_):
    self._more[name_] = value_

  def setPenetration(self, name_, value_):
    self._penetration[name_] = value_

  def setAttribute(self, name_, value_):
    self._attribute[name_] = value_

  def setDuration(self, name_, modifier_, value_):
    self._duration[name_][modifier_] = value_

  def setTrigger(self, name_, modifier_, value_):
    self._trigger[name_][modifier_] = value_

  def getIncreaseByTagList(self, tags_):
    return sum([self.getIncrease(t) for t in tags_])

  def getMoreByTagList(self, tags_):
    return prod([self.getMore(t) for t in tags_])


############################################################################################
# Additional constructor functions
############################################################################################

def fromBuff(durationContainer_):
  modifier = Modifier()
  for buff in durationContainer_.getActiveWithType('buff'):
    modifier += buff.getModifier()

  return modifier
