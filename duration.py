from data import durationData

import errors, stats

from numpy import isclose, product as prod

from itertools import chain

class Duration():

  def __init__(self, name_, stats_, tempStats_ = None, skillAttributes_ = []):
    if name_ not in durationData.keys():
        raise errors.InvalidDurationError
    else:
        self.name = name_

    # get ailment damage values
    self.baseDuration = durationData[self.name]['baseDuration']
    self.duration = self.baseDuration
    self.duration *= (1. + stats_.duration[self.name]['duration'])
    self.elapsed = 0

    # skip remaining part for non-damaging ailments
    if durationData[self.name]['type'] != 'damagingAilment':
      return

    self.baseDamage = durationData[self.name]['baseDamage']
    self.damage = self.baseDamage
    self.damage *= (1. + stats_.duration[self.name]['effect'])

    # additional scaling attribute provided by applying skill, i.e., strength, dexterity
    self.skillAttributes = skillAttributes_

    # attribute scaling is assumed to be always 4%
    increase = sum([stats_.increase[a] for a in durationData[self.name]['tags']]) \
                + 0.04 * sum([stats_.attribute[a] for a in self.skillAttributes])
    more = prod([stats_.more[a] for a in durationData[self.name]['tags']])

    # add temporary stats, e.g., from buffs, if provided
    if tempStats_ != None:
      increase += sum([tempStats_.increase[a] for a in durationData[self.name]['tags']])
      more *= prod([tempStats_.more[a] for a in durationData[self.name]['tags']])

    # print(increases)
    # print(more)

    self.damage *= (1 + increase) * more

    pass

  def getName(self):
    return self.name

  def getSkillAttributes(self):
    return self.skillAttributes

  def active(self):
    # return self.elapsed != self.duration
    return not isclose(self.elapsed, self.duration, rtol=0, atol=1e-2, equal_nan=False)

  def tick(self, timestep):
    # ailment falls off within 'timestep' -> set timestep size and elapsed timer accordingly
    # maybe the check should be whether the next tick with same timestep will provide another full tick
    if self.elapsed + timestep >= self.duration:
        timestep = self.duration - self.elapsed
        self.elapsed = self.duration
    # increase elapsed timer
    else:
        self.elapsed += timestep

    # if non-damaging ailment leave here
    if durationData[self.getName()]['type'] != 'damagingAilment':
        return 0

    # return resulting damage
    # note: assumes scaling with duration which is could be changed
    # it seems that the quotient of
    # (self.baseDamage / self.baseDuration)
    # is uneffected by duration increases and thus duration increases yield more ticks of the same value
    return (self.damage / self.baseDuration) * timestep

class Durations():

  def __init__(self, stats, verbosity):

    self.buffs = []
    self.shreds = []
    self.damagingAilments = []
    self.cooldowns = []


    self.stats = stats
    self.verbosity = verbosity
    pass

  def add(self, name_, tempStats_ = None, skillAttributes_ = []):

    # ailment application consideres increases/more as well as effects on application
    durationType = durationData[name_]['type']

    # store ailment accodingly
    if durationType == 'shred':
      self.shreds.append(Duration(name_, self.stats, skillAttributes_ = skillAttributes_))
    elif durationType == 'buff':
      self.buffs.append(Duration(name_, self.stats, skillAttributes_ = skillAttributes_))
    elif durationType == 'cooldown':
      self.cooldowns.append(Duration(name_, self.stats, skillAttributes_ = skillAttributes_))
    elif durationType == 'damagingAilment':
    # todo: consider buffs here and pass them as additional increase/more modifiers
    # they seem to be snapshotted on application

      # add buffs up together for in stat container increase/more/etc
      # todo should possible only be calculated once per tick instead per add-call -> move to tick?
      buffStats = stats.Stats(self.buffs)

      self.damagingAilments.append(Duration(name_, self.stats, tempStats_ = buffStats, skillAttributes_ = skillAttributes_))
      if name_ == 'poison':
        self.shreds.append(Duration('poisonBuiltinShred', self.stats, skillAttributes_ = skillAttributes_))

  def getActive(self, type = None):
    # return active iterators for ailments of specific type, similar to but more efficient than [a for a in self.durations if a.active()]
    if type != None:
        return filter(lambda a: a.active() and durationData[a.getName()]['type'] == type, self.getByType(type))
    else:
        return filter(lambda a: a.active(), self.getByType(type))

  def getAll(self):
    return self.getByType()

  def getByType(self, type = None):
    if type == None:
      return chain(self.shreds, self.damagingAilments, self.buffs, self.cooldowns)
    elif type == 'shred':
      return self.shreds
    elif type == 'buff':
      return self.buffs
    elif type == 'damagingAilment':
      return self.damagingAilments
    elif type == 'cooldown':
      return self.cooldowns

  def removeInactive(self):
    # remove expired ailments, .e.g, only keep active ones
    # slicing does not involve reallocation as stated here: https://stackoverflow.com/a/1208792
    self.buffs[:] = [b for b in self.buffs if b.active()]
    self.shreds[:] = [s for s in self.shreds if s.active()]
    self.damagingAilments[:] = [a for a in self.damagingAilments if a.active()]
    pass

  def countActive(self, type = None, sparse = True):
    # todo: keys only for durationData corresponding to type to reduce overhead
    active = dict.fromkeys(durationData.keys(), 0)
    for a in self.getActive(type):
            active[a.getName()] += 1
    if sparse:
      return {x:y for x,y in active.items() if y != 0}
    else:
      return active

  def tick(self, timestep, boss = False):

    # for damage calculation non-damaging ailments (currently shreds only) must be count first
    # and maxStacks must be considered
    # poison currently just applies poisonShred for 3s as well (todo: check if there is a source of 4s poisonShred)
    # Q&A
    # 1) Are ailments over limit still applied but inactive until others are expired?
    # gameguide -> it replaces the oldest one. Means can just be added; deleting them would be to much overhead

    if self.verbosity >= 2:
        print(self.countActive())

    # get active shred counts
    shreds = self.countActive("shred")
    # print(shreds)

    damage = 0
    tick_damage = 0

    for a in self.getAll():
      # damage = basedamage (scaled by ailment effect/duration) * (sum(increases) + sum(attribute increases) * prod(more)
      #          * others
      # everything besides others is already considered when ailments are applied ant hus snappshotted

      # process ailment
      damage = a.tick(timestep)

      # skip following calculations if it is a non-damaging ailment
      if durationData[a.getName()]['type'] != 'damagingAilment':
        continue

      # element type of current damaging ailment
      element = durationData[a.getName()]['element']
      # get active shreds associated with element type 'element'
      relevantShreds = list(filter(lambda a: durationData[a]['element'] == element, shreds))

      # shred
      shred = 0.

      # add elemental shred shred, limited by maxStack
      # relevantShreds mostly have only one entry; for poison there are two shreds!
      # built in poison shred does not have a stack limit and goes along poisonShred
      for i in relevantShreds:
          # limit shred if necessary
          shred += (min(shreds[i], durationData[i]['maxStack']) if durationData[i]['maxStack'] != 0 else shreds[i])
          # print(shreds[i])
          # print(durationData[i]['maxStack'])
      # active_stacks
      # print(relevantShreds) # must cast relevantShreds to list when receiving applying filter
      # print(shred)
      # self.stats.penetration[element]

      # penetration as sum of shred an gear affixes
      # 1 shred stack reduces resist by 5%
      # shred effect is reduced by 60% for bosses
      penetration = shred * 0.05 * (0.4 if boss else 1.) + self.stats.penetration[element]

      # scale damage with penetration; add enemey conditions as well for resistances and maybe block
      damage *= (1. + penetration)


      tick_damage += damage
      # print('{} dealt {} damage over {} seconds'.format(a.getName(), damage, timestep))

    # print(tick_damage)
    # removes inactive ailments
    self.removeInactive()

    return tick_damage