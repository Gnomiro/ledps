import duration, skill, character, equipment

import copy

class Collection():
  """docstring for Collection"""
  def __init__(self):

    self._character = None
    self._equipment = None

    self._skillCollection = {}
    self._durationCollection = {}
    pass

  def getCharacter(self):
    if self._character is None:
      self._character = character.Paladin()
    return self._character

  def getCharacterModifier(self):
    return self.getCharacter().getModifier()

  def getEquipment(self):
    if self._equipment is None:
      self._equipment = equipment.Equipment()
    return self._equipment

  def getEquipmentModifier(self):
    return self.getEquipmentModifier().getModifier()

  def getPersistentModifier(self):
    return self.getEquipmentModifier() + self.getCharacterModifier()

  def getDuration(self, name_):
    if name_ not in self._durationCollection:
      self._durationCollection[name_] = duration.getDefaultObjectByName(name_)
    return self._durationCollection[name_]

  def getSkill(self, name_):
    if name_ not in self._skillCollection:
      self._skillCollection[name_] = skill.getDefaultObjectByName(name_)
      self._skillCollection[name_].setCollection(self)
    return self._skillCollection[name_]

  def getSkills(self):
    return self._skillCollection

  def getSkillOnTheFly(self, name_, durationContainer_):
    print('Warning: Collection getSkillOnTheFly not implemented yet.')
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

