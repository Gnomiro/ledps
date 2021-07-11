import duration, skill, character, equipment, error

import copy

class Collection():
  """docstring for Collection"""
  def __init__(self):

    self._character = None
    self._equipment = None

    self._skillCollection = {}
    self._durationCollection = {}

    self._prepared = False
    pass

  def prepare(self):
    if not self._prepared:
      self._character.prepare()
      # todo: do similar things for skills as they also have duration objects they change globally
      self._character.applyModification(self)
      for s in self._skillCollection.values():
        s.applyModification(self)
      self._prepared = True
    pass

  def resetDurationCollection(self):
    self._durationCollection = {}
    self._prepared = False
    pass

  def setCharacter(self, name_):
    if self._character is not None:
      print('Warning: Previously selected class is replaced!')
    # todo: make this more smart; get available classes like available duration/skills
    if name_ in ['paladin', 'beastmaster']:
      characterClass = name_[0].upper() + name_[1:]
      self._character = eval('character.' + characterClass)()
    else:
      raise error.UnsupportedClass(name_)
    return self._character

  def getCharacter(self):
    if self._character is None:
      raise error.UnsupportedClass('NoClass')
    return self._character

  def getCharacterModifier(self):
    return self.getCharacter().getModifier()

  def getEquipment(self):
    if self._equipment is None:
      self._equipment = equipment.Equipment()
    return self._equipment

  def getEquipmentModifier(self):
    return self.getEquipment().getModifier()

  def getPersistentModifier(self):
    return self.getEquipmentModifier() + self.getCharacterModifier()

  def getDuration(self, name_):
    if name_ not in self._durationCollection:
      self._durationCollection[name_] = duration.getDefaultObjectByName(name_)
    return self._durationCollection[name_]

  def getDurationCopy(self, name_):
    if name_ not in self._durationCollection:
      self._durationCollection[name_] = duration.getDefaultObjectByName(name_)
    return copy.deepcopy(self._durationCollection[name_]) # todo: implement a simple copy routine which creates a copy with copies of only relevant objects

  def getSkill(self, name_):
    if name_ not in self._skillCollection:
      self._skillCollection[name_] = skill.getDefaultObjectByName(name_)
      self._skillCollection[name_].setCollection(self)
    return self._skillCollection[name_]

  def getSkills(self):
    return self._skillCollection

  def getSkillOnTheFly(self, name_, durationContainer_):
    if name_ not in self._skillCollection:
      self.getSkill(name_)
      self._skillCollection[name_].setDurationContainer(durationContainer_)
    return self._skillCollection[name_]


  # todo: what to really keep in here? Also current buffs and other stuff???
  # maybe even durations instead of tracking them in the durationsContainer?
  # collect everything here and provide routines which check for changes
  # def getModifier(self):
  #   pass

  # def updateModifier(self):
  #   pass

