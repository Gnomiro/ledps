import duration

import copy

class Collection():
  """docstring for Collection"""
  def __init__(self):
    self._skillLibrary = {}
    self._durationLibrary = {}
    pass

  def getDuration(self, name_):
    if name_ not in self._durationLibrary:
      self._durationLibrary[name_] = duration.getDefaultDuration(name_)
    return self._durationLibrary[name_]



  # todo: what to really keep in here? Also current buffs and other stuff???
  # maybe even durations instead of tracking them in the durationsContainer?
  # collect everything here and provide routines which check for changes
  # def getModifier(self):
  #   pass

  # def updateModifier(self):
  #   pass

