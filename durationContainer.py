import collection, error, duration, element

from itertools import chain

verbosity = 2

class DurationContainer():
  """docstring for DurationContainer"""
  def __init__(self, collection_):

    self._durations = {}

    self._collection = collection_
    pass


  def add(self, name_, modifer_):


    duration = self._collection.getDurationCopy(name_)
    duration.applyModifier(modifer_)

    if name_ not in self._durations.keys():
      self._collection[name_] = list([])

    if d.hasStackLimit() and self.countActiveByName(d.getName()) >= d.getMaxStacks():
      if verbosity >= 2:
        print('Limit of {} reached; replace oldest'.format(name_))

      _, idx = min( ( (d.getRemainingDuration(), idx) for (idx, d) in enumerate(self._durations[name_]) ) )
      self._durations[name_][idx] = duration
    else:
      self._durations[name_].append(duration)

    pass

  def addCooldown(self, name_, duration_):

    if 'cooldown' not in self._durations.keys():
      self._durations['cooldown'] = list([])

    if name_ in [c.getName() for c in self.getActiveByName('cooldown')]: # self.getActiveByType('cooldown') should also work for cooldown
      return False
    else:
      self._durations['cooldown'] = duration.Cooldown(name_ = name_, duration_ = duration_)
      return True

  def tick(self, timestep_, modifer_):

    damage = element.ElementContainer()

    for d in self.getAll():

      _, dmg = d.tick(timestep_)

      if dmg is not None:
        damage += dmg


    print('Warning: No penetration yet. Collect damage per skill and apply penentration at the end.')

    self.removeInactive()

    return damage

  def removeInactive(self):
    # remove expired durations in each list, .i.e, only keep active ones
    # slicing does not involve reallocation as stated here: https://stackoverflow.com/a/1208792
    for name in self._durations.keys():
      self._durations[name][:] = [d for d in self._durations[name] if d.isActive()]
    pass

  def getAll(self):
    return self._durations

  def getByType(self, type_):
    return self.getByTypes(type_)

  def getByTypes(self, *types_):
    if not types_:
      return self.getAll()
    elif all([t in duration.getBaseClasses() for t in types_]):
      return [d for d in chain.from_iterable(self._durations) if any(d.hasType(t) for t in types_)]
    else:
      raise error.InvalidDurationType(types_)

  def getByName(self, name_):
    return self.getByNames(name_)

  def getByNames(self, *names_):
    if not names_:
      return self.getAll()
    elif all([n in duration.getImplementedClasses() for n in names_]):
      return chain.from_iterable([self._durations[n] for n in names_])
    else:
      raise error.InvalidDuration(names_)

  def getActive(self):
    return filter(lambda a: a.isActive(), self.getAll())

  def getActiveByType(self, type_):
    return filter(lambda a: a.isActive(), self.getByType(type_))

  def getActiveByTypes(self, *types_):
    return filter(lambda a: a.isActive(), self.getByTypes(*types_))

  def getActiveByName(self, name_):
    return filter(lambda a: a.isActive(), self.getByName(name_))

  def getActiveByNames(self, *names_):
    return filter(lambda a: a.isActive(), self.getByNames(*names_))

  def countActiveByName(self, name_):
    return self.countActiveByNames(name_)

  def countActiveByNames(self, *names_):
    active = {}
    for a in self.getActiveByNames(*names_):
      active[a.getName()] = active.get(a.getName(), 0) + 1
    return active

  def countActiveByType(self, type_):
    return self.countActiveByTypes(type_)

  def countActiveByTypes(self, *types_):
    active = {}
    for a in self.getActiveByTypes(*types_):
      active[a.getName()] = active.get(a.getName(), 0) + 1
    return active

  def countActive(self):
    active = {}
    for a in self.getAll():
      active[a.getName()] = active.get(a.getName(), 0) + 1
    return active