import collection, error, duration, element

from itertools import chain

verbosity = 0

class DurationContainer():
  """docstring for DurationContainer"""
  def __init__(self, collection_):

    self._durations = {}

    self._collection = collection_
    pass


  def add(self, name_, modifier_, skillName_ = None, skillN_ = None):

    duration = self._collection.getDurationCopy(name_)
    duration.applyModifier(modifier_)

    if skillName_ is not None and skillN_ is not None:
      duration.setAppliedBy(skillName_, skillN_)

    if name_ not in self._durations.keys():
      self._durations[name_] = list([])

    if duration.hasStackLimit() and self.countActiveByName(name_)[name_] >= duration.getMaxStacks():
      if verbosity >= 1:
        print('Limit of {} reached; replace oldest'.format(name_))

      _, idx = min( ( (duration.getRemainingDuration(), idx) for (idx, d) in enumerate(self._durations[name_]) ) )
      self._durations[name_][idx] = duration
    else:
      self._durations[name_].append(duration)

    pass

  def addCooldown(self, name_, duration_):

    if duration_ == 0:
      return True

    if 'cooldown' not in self._durations.keys():
      self._durations['cooldown'] = list([])

    if name_ in [c.getName() for c in self.getActiveByName('cooldown')]: # self.getActiveByType('cooldown') should also work for cooldown
      return False
    else:
      self._durations['cooldown'].append(duration.Cooldown(name_ = name_, duration_ = duration_))
      return True

  def tick(self, timestep_, modifier_):

    damage = element.ElementContainer()

    damageBySkill = {}

    for d in self.getActive():

      _, dmg = d.tick(timestep_)

      if dmg is not None:

        skillName, skillN = d.getAppliedBy()

        if skillName not in damageBySkill.keys():
          damageBySkill[skillName] = {}

        if skillN not in damageBySkill[skillName].keys():
          damageBySkill[skillName][skillN] = element.ElementContainer()

        damageBySkill[skillName][skillN] += dmg

    for skillName, skill in damageBySkill.items():
      for skillN, skillDamage in skill.items():

        # penetration
        # applied for hits seperately
        resistances = element.ElementContainer(default_ = 0.0)
        allModifier = modifier_ + self._collection.getSkill(skillName).getSkillModifier(skillN)
        penetration = element.ElementContainer(default_ = 0.0, **allModifier.getPenetrations())
        shred = element.fromResistanceShred(self)
        resistances -= shred
        resistances.setUpperLimit(0.75)
        penetration -= resistances
        skillDamage.imultiply(penetration, shift_ = 1.0)

        # sum up damage
        damage += skillDamage

    self.removeInactive()

    return damage

  def removeInactive(self):
    # remove expired durations in each list, .i.e, only keep active ones
    # slicing does not involve reallocation as stated here: https://stackoverflow.com/a/1208792
    for name in self._durations.keys():
      self._durations[name][:] = [d for d in self._durations[name] if d.isActive()]
    pass

  def getAll(self):
    return chain.from_iterable(self._durations.values())

  def getByType(self, type_):
    return self.getByTypes(type_)

  def getByTypes(self, *types_):
    if not types_:
      return self.getAll()
    elif all([t in duration.getBaseClasses() for t in types_]):
      # old and slower: return [d for d in chain.from_iterable(self._durations.values()) if any(d.hasType(t) for t in types_)]
      return chain.from_iterable([self._durations[k] for k in self._durations.keys() if len(self._durations[k]) != 0 and any(self._durations[k][0].hasType(t) for t in types_)])
    else:
      raise error.InvalidDurationType(types_)

  def getByName(self, name_):
    return self.getByNames(name_)

  def getByNames(self, *names_):
    if not names_:
      return self.getAll()
    elif all([n in duration.getImplementedClasses() for n in names_]):
      return chain.from_iterable([self._durations[n] for n in names_ if n in self._durations.keys()])
    else:
      raise error.InvalidDuration(names_)

  def getActive(self):
    return filter(lambda a: a.isActive(), self.getAll())

  def getActiveWithType(self, type_):
    return filter(lambda a: a.isActive(), self.getByType(type_))

  def getActiveWithTypes(self, *types_):
    return filter(lambda a: a.isActive(), self.getByTypes(*types_))

  def getActiveByName(self, name_):
    return filter(lambda a: a.isActive(), self.getByName(name_))

  def getActiveByNames(self, *names_):
    return filter(lambda a: a.isActive(), self.getByNames(*names_))

  def countActiveByName(self, name_):
    return self.countActiveByNames(name_)

  def countActiveByNames(self, *names_):
    active = dict.fromkeys(names_, 0)
    for a in self.getActiveByNames(*names_):
      active[a.getName()] = active.get(a.getName(), 0) + 1
    return active

  def countActiveWithType(self, type_):
    return self.countActiveWithTypes(type_)

  def countActiveWithTypes(self, *types_):
    active = {}
    for a in self.getActiveWithTypes(*types_):
      active[a.getName()] = active.get(a.getName(), 0) + 1
    return active

  def countActive(self):
    active = {}
    for a in self.getAll():
      active[a.getName()] = active.get(a.getName(), 0) + 1
    return active