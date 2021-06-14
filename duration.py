from numpy import isclose, product as prod
from itertools import chain

import data
import errors
import stats
import damage

#########################################################################################################
# Generic duration class
#########################################################################################################

# duration object; can be any type of supported duration based buff/debuff/cooldown
class Duration():

  # create duration object; by default requires duration 'name_' string only;
  # for damagingAilments gearStats_ as well as tmpStats_ (e.g., buffs) can be passed
  # as they are snappshotted at application time
  # 'skillAttributes_' provide the attributes of the applying skill as they scale the damagingAilments as well
  # skill cooldowns can be passed by specifying 'duration_' and 'type_ = 'cooldown''; otherwise these values are ignored
  def __init__(self, name_, gearStats_ = stats.Stats(), tmpStats_ = stats.Stats(), skillAttributes_ = [], duration_ = None, type_ = None):

    if name_ in data.getDurationData().keys():
      # default duration behaviour; determined by name_; duration_ and type_ are ignored
      if duration_ != None or type_ != None:
        print("Warning: duration_ and type_ input are ignored")
      self._type = data.getDurationData()[name_]['type']
      self._baseDuration = data.getDurationData()[name_]['baseDuration']
      self._duration = self._baseDuration
      self._duration *= (1. + gearStats_.duration[name_]['duration'])

    elif duration_ != None and type_ == 'cooldown' and name_ in data.getSupportedSkills():
      # duration is a skill-specific cooldown
      self._type = type_
      self._baseDuration = duration_
      self._duration = self._baseDuration

    else:
      print(name_)
      # raise error since unsupported parameters are passed
      raise errors.InvalidDurationError

    # duration name
    self._name = name_

    # elapsed time
    self._elapsed = 0

    # skip remaining part for non-damaging ailments
    if self.getType() != 'damagingAilment':
      return

    # additional scaling attribute provided by applying skill, i.e., strength, dexterity
    self._skillAttributes = skillAttributes_

    # scale damage by ailment specific modifiers
    self._baseDamage = data.getDurationData()[self.getName()]['baseDamage']
    self._damage = self._baseDamage
    self._damage *= (1. + gearStats_.duration[self.getName()]['effect'])

    #print(data.getDurationData()[self.getName()]['tags'])

    # get sum of relevant increase modifiers
    increase = gearStats_.getIncreaseByTagList(data.getDurationData()[self.getName()]['tags']) + tmpStats_.getIncreaseByTagList(data.getDurationData()[self.getName()]['tags'])
    # general attribute-scaling for damagingAilment; assumed to be always 4%; todo: check if sometimes different
    increase += 0.04 * sum([gearStats_.attribute[a] for a in self._skillAttributes])

    # get product of relevant more modifiers
    more = gearStats_.getMoreByTagList(data.getDurationData()[self.getName()]['tags']) * tmpStats_.getMoreByTagList(data.getDurationData()[self.getName()]['tags'])

    # final overall damage of damagingAilment
    self._damage *= (1. + increase) * more

    pass

  # return remaining duration
  # todo: review behaviour for infinite buffs
  def getRemainingDuration(self):
    return self._duration - self._elapsed

  # returns duration name
  def getName(self):
    return self._name

  # returns duration type
  def getType(self):
    return self._type

  # tells if the duration object has unlimited duration
  # duration buffs with _duration == -1 are assumed to have unlimited duration
  def isPermanent(self):
    return bool(1 if self._duration == -1 else 0)

  # returns state of duration buff
  def isActive(self):
    if self.isPermanent():
      return True
    else:
      return not isclose(self._elapsed, self._duration, rtol = 0, atol = 1e-2, equal_nan = False)

  # processes the next tick of the duration buff considering a stepsize of 'timestep_'
  def tick(self, timestep_):
    # check if duration falls of within calculation timestep_
    # todo: maybe the check should be whether the next tick with same timestep will provide another full tick
    if not self.isPermanent() and self._elapsed + timestep_ >= self._duration:
      # ailment falls off within 'timestep' -> set timestep size and elapsed timer accordingly to acquire accurate damage
        timestep_ = self._duration - self._elapsed
        self._elapsed = self._duration
    # increase elapsed timer
    else:
        self._elapsed += timestep_

    # if duration is not a damagingAilment return 0 damage object and leave
    if self._type != 'damagingAilment':
        return damage.Damage()

    # return resulting damage
    # note: assumes scaling with duration which could be changed
    # it seems that the quotient of
    # (self.baseDamage / self.baseDuration)
    # is uneffected by duration increases and thus duration increases yield more ticks of the same value
    return damage.Damage((data.getDurationData()[self.getName()]['element'], self._damage / self._baseDuration * timestep_))

#########################################################################################################
# Container for duration class objects seperating them by type
#########################################################################################################

# container class managing all duration objects
class Durations():

  # constructor; expecting gearStats for scaling behaviour
  def __init__(self, gearStats_ = stats.Stats(), verbosity_ = 0):

    # does not work as it points to the same lists in every dict: self._durations = dict.fromkeys(data.getSupportedDurationTypes(), [])
    self._durations = {key : [] for key in data.getSupportedDurationTypes()}

    self._gearStats = gearStats_
    self._verbosity = verbosity_

    pass

  # add an ailment
  def add(self, name_, skillAttributes_ = [], duration_ = None, type_ = None):

    # allocate buffs into temporary stats object if duration-type is of damagingAilment -> snapshotting
    if name_ in data.getDurationData().keys() and data.getDurationData()[name_]['type'] == 'damagingAilment':
      tmpStats = stats.Stats().fromBuffs(self)
    else:
      tmpStats = stats.Stats()

    # create duration object; passing all stats
    duration = Duration(name_, gearStats_ = self._gearStats, tmpStats_ = tmpStats, skillAttributes_ = skillAttributes_, duration_ = duration_, type_ = type_)

    # replace oldest duration if it is not a cooldown and has a maxStack size otherwise just add it
    if duration.getType() != 'cooldown' and data.getDurationData()[duration.getName()]['maxStack'] != 0 and self.countActiveByNames(duration.getName())[duration.getName()] >= data.getDurationData()[duration.getName()]['maxStack']:
      if self._verbosity >= 2:
        print('Limit of {} reached; replace oldest'.format(duration.getName()))

      # get idx of oldest duration buff of requested type to replace it
      _, idx = min(((d.getRemainingDuration(), idx) if d.getName() == duration.getName() else (float('inf'), idx)) for (idx, d) in enumerate(self._durations[duration.getType()]))
      self._durations[duration.getType()][idx] = duration
      return
    else:
      # add new duration
      self._durations[duration.getType()].append(duration)

    # poison applies a build in poison shred as well which has not stack limitation
    if duration.getType() == 'damagingAilment' and duration.getName() == 'poison':
      self._durations['shred'].append(Duration('poisonBuiltinShred', self._gearStats, skillAttributes_ = skillAttributes_))

    pass

  # todo: addMultiple for better ressource management when applying more than one of the same duration

  def removeInactive(self):
    # remove expired durations in each list, .i.e, only keep active ones
    # slicing does not involve reallocation as stated here: https://stackoverflow.com/a/1208792
    for key in self._durations.keys():
      self._durations[key][:] = [d for d in self._durations[key] if d.isActive()]
    pass

  # get durations specified by type-list
  def getByTypes(self, *type_):
    if not type_:
      return chain.from_iterable(self._durations.values())
    elif all([t in data.getSupportedDurationTypes() for t in type_]):
      return chain.from_iterable([self._durations[t] for t in type_])
    else:
      raise errors.InvalidDurationError

  # get active durations specified by type-list
  def getActiveByTypes(self, *type_):
    # return active iterators for ailments of specific type, similar to but more efficient than [a for a in self.durations if a.active()]
    return filter(lambda a: a.isActive(), self.getByTypes(*type_))

  # count active durations specified by type-list
  def countActiveByTypes(self, *type_):
    active = {}
    for a in self.getActiveByTypes(*type_):
      active[a.getName()] = active.get(a.getName(), 0) + 1
    return active

  # get durations specified by name-list
  def getByNames(self, *name_):
    if not name_:
      return chain.from_iterable(self._durations.values())
    elif all([n in data.getSupportedDurations() for n in name_]):
      return [d for d in chain.from_iterable(self._durations.values()) if d.getName() in name_]
    else:
      raise errors.InvalidDurationError

  # get active durations specified by name-list
  def getActiveByNames(self, *name_):
    # return active iterators for ailments of specific type, similar to but more efficient than [a for a in self.durations if a.active()]
    return filter(lambda a: a.isActive(), self.getByNames(*name_))

  # count active durations specified by name-list
  def countActiveByNames(self, *name_):
    # dict always contains requested counts even when they are 0
    active = dict.fromkeys(name_, 0)
    for a in self.getActiveByNames(*name_):
      active[a.getName()] = active.get(a.getName(), 0) + 1
    return active

  # count all active durations
  def countActive(self):
    return self.countActiveByTypes()

  # get all durations
  def getAll(self):
    return self.getByTypes()

  # process next tick for all durations; calculating damage
  def tick(self, timestep_ = 0.1, boss_ = False):

    if self._verbosity >= 2:
        print(self.countActive())

    # create empty damage object
    tick_dmg = damage.Damage()

    # loop over all duration objects
    for d in self.getAll():
      # process duration object, receive damage and accumulate it
      tick_dmg += d.tick(timestep_)

    # get penetration from gearStats_ and normalize it to 1. to multiply damage values later
    penetration = {k: (self._gearStats.penetration[k] + 1.) for k in self._gearStats.penetration}
    # print(penetration)
    # count active shreds and add them to penetration from gear
    shreds = self.countActiveByTypes('shred')
    for key in shreds:
      penetration[data.getDurationData()[key]['element']] += shreds[key] * 0.05 * (0.4 if boss_ else 1.)
    # print(penetration)
    # scale damage by penetration
    tick_dmg.multiplyEachElementSeperately(penetration)

    # removes inactive duration objects
    self.removeInactive()

    # return damage of durations during timestep
    return tick_dmg