from math import floor, ceil

from itertools import cycle

import stats
import random
random.seed()

enemies = 1
print("Enemies hit: " + str(enemies))

class Rive():

  def __init__(self, cadence = False, flurry = 0, indomitable = False, sever = 0, twistingFangs = 0, execution = False):

    self.attacktimes = [0.68182, 0.68182, 0.68182]
    self.nAttacktimes = len(self.attacktimes)
    # local skill specific stats for each of the free attacks
    self.stats = [stats.Stats() for i in range(self.nAttacktimes)]

    self.skillAttributes = ['strength']

    if flurry != 0:
      self.stats[0].increase['meleeAttackSpeed'] += 0.08 * flurry
      self.stats[1].increase['meleeAttackSpeed'] += 0.08 * flurry

    if sever != 0:
      self.stats[0].duration['ignite']['onHit'] += 0.5 * sever

    if twistingFangs != 0:
      self.stats[1].duration['ignite']['onHit'] += 0.5 * twistingFangs

    # next(self.sequence) returns following attack
    if not cadence:
      self.sequence = cycle([0, 1, 2])
    else:
      self.sequence = cycle([0, 1, 0, 1, 2])

    # stores current position in sequence
    self.n = next(self.sequence)

    # todo: additional hit on first strike
    self.indomitable = indomitable

    # for ignite conversion
    self.execution = execution

    pass


  # attack, returns next attack time (currently default)
  # todo: possible refactor and put ailment application and strike procs into general skill-independent class-functions
  def attack(self, durations_, stats_ = None, tempStats_ = None):

    # todo: make stat additive and simplify loop only over relevant entries instead of continue
    # for ailment, info in filter(lambda a: a[1]['onHit'] != 0, stats_.duration.items()):

    for ailment, info in stats_.duration.items():

      # add skill specific chances, i.e., ignite chance for rive if skilled
      chance = info['onHit'] + self.stats[self.n].duration[ailment]['onHit']

      if chance == 0:
        continue

      # guaranteed applications
      applications = floor(chance)

      # if hit chance not equal onHit chance roll if additional applications happen
      if applications != chance and random.random() <= chance - applications:
        # print('{} added by chance'.format(ailment))
        applications += 1
      # one bleed for each application
      for i in range(applications):
        durations_.add(ailment, skillAttributes_ = self.skillAttributes)

    # assumes that buff creation is after ignite removal, damage tick and only applies to following hits
    if self.execution and self.n == 2:
      # number of active ignite, multiplied by enemies
      nIgnites = durations_.countActive(type = 'damagingAilment', sparse = False)['ignite'] * enemies
      # removes all ignite debuffs and adds a number of riveExecution buffs
      durations_.damagingAilments[:] = [a for a in durations_.damagingAilments if a.getName() != 'ignite']
      for i in range(nIgnites):
        durations_.add('riveExecution')
        pass

    # update sequence position after hit
    self.n = next(self.sequence)

    # procs like manifest strike
    for proc, info in stats_.proc.items():
      # add skill specific chances, i.e., ignite chance for rive if skilled
      chance = info['onHit'] + self.stats[self.n].proc[proc]['onHit']

      # guaranteed applications
      applications = floor(chance)

      # if hit chance not equal onHit chance roll if additional applications happen
      if applications != chance and random.random() <= chance - applications:
        # print('{} added by chance'.format(ailment))
        applications += 1
      for i in range(applications):
        # eval(proc) calls constructor of relevant attack
        # todo: maybe pass stats and others as well
        _, attacktime, durations_ = eval(proc)().attack(durations_, stats_)
        # _, attacktime, durations_ = ManifestStrike().attack(durations_, stats_)


    # pass damage, next attack speed as well as possibly modified durations (applied ailments and buffs)
    return 0, self.getAttacktime(stats_, tempStats_), durations_

  def getAttacktime(self, stats_ = None, tempStats_ = None):

    if stats_ != None:
      return self.attacktimes[self.n] / (1 + stats_.increase['meleeAttackSpeed'] + self.stats[self.n].increase['meleeAttackSpeed']) / (stats_.more['meleeAttackSpeed'] * self.stats[self.n].more['meleeAttackSpeed'])
    else:
      return self.attacktimes[self.n]


class Warpath():

  def __init__(self, warForge = 0, moltenPath = 0):

    # warpath has half the attacktime; through multiplication order does not matter
    # reduced ailment chance is handled in attack-skill
    self.attacktimes = [0.68182 / 2.]
    self.nAttacktimes = len(self.attacktimes)
    # local skill specific stats for each of the free attacks
    self.stats = [stats.Stats() for i in range(self.nAttacktimes)]

    self.skillAttributes = ['strength']

    if warForge != 0:
      self.stats[0].duration['ignite']['onHit'] += 0.06 * warForge
      # warpath hits only
      # self.stats[0].penetration['fire'] += 0.06 * warForge
      # self.stats[0].penetration['physical'] += 0.06 * warForge

    if moltenPath != 0:
      # warpath hits only
      # self.stats[0].duration['ignite']['onHit'] += 0.08 * moltenPath
      pass

    self.sequence = cycle([0])

    # stores current position in sequence
    self.n = next(self.sequence)

    pass


  # attack, returns next attack time (currently default)
  # todo: possible refactor and put ailment application and strike procs into general skill-independent class-functions
  def attack(self, durations_, stats_ = None, tempStats_ = None):

    # todo: make stat additive and simplify loop only over relevant entries instead of continue
    # for ailment, info in filter(lambda a: a[1]['onHit'] != 0, stats_.duration.items()):

    for ailment, info in stats_.duration.items():

      # add skill specific chances, i.e., ignite chance for rive if skilled
      # including warpath global ailment reduction chance
      chance = info['onHit'] + self.stats[self.n].duration[ailment]['onHit'] * 0.6

      if chance == 0:
        continue

      # guaranteed applications
      applications = floor(chance)

      # if hit chance not equal onHit chance roll if additional applications happen
      if applications != chance and random.random() <= chance - applications:
        # print('{} added by chance'.format(ailment))
        applications += 1
      # one bleed for each application
      for i in range(applications):
        durations_.add(ailment,  skillAttributes_ = self.skillAttributes)

    # update sequence position after hit
    self.n = next(self.sequence)

    # procs like manifest strike
    for proc, info in stats_.proc.items():
      # add skill specific chances, i.e., ignite chance for rive if skilled
      chance = info['onHit'] + self.stats[self.n].proc[proc]['onHit']

      # guaranteed applications
      applications = floor(chance)

      # if hit chance not equal onHit chance roll if additional applications happen
      if applications != chance and random.random() <= chance - applications:
        # print('{} added by chance'.format(ailment))
        applications += 1
      for i in range(applications):
        # eval(proc) calls constructor of relevant attack
        # todo: maybe pass stats and others as well
        _, attacktime, durations_ = eval(proc)().attack(durations_, stats_)
        # _, attacktime, durations_ = ManifestStrike().attack(durations_, stats_)


    # pass damage, next attack speed as well as possibly modified durations (applied ailments and buffs)
    return 0, self.getAttacktime(stats_, tempStats_), durations_

  def getAttacktime(self, stats_ = None, tempStats_ = None):

    if stats_ != None:
      return self.attacktimes[self.n] / (1 + stats_.increase['meleeAttackSpeed'] + self.stats[self.n].increase['meleeAttackSpeed']) / (stats_.more['meleeAttackSpeed'] * self.stats[self.n].more['meleeAttackSpeed'])
    else:
      return self.attacktimes[self.n]


# Manifest Strike for proccs
class ManifestStrike():

  def __init__(self):
    # print('ManifestStrike')
    self.attacktimes = [0.]
    self.nAttacktimes = len(self.attacktimes)
    # local skill specific stats for each of the free attacks

    self.skillAttributes = []

    self.stats = [stats.Stats() for i in range(3)]

    self.sequence = cycle([0])

    # stores current position in sequence
    self.n = next(self.sequence)

    pass

  def attack(self, durations_, stats_ = None, tempStats_ = None):

    for ailment, info in stats_.duration.items():

      # add skill specific chances, i.e., ignite chance for rive if skilled
      chance = info['onHit'] + self.stats[self.n].duration[ailment]['onHit']

      if chance == 0:
        continue

      # guaranteed applications
      applications = floor(chance)

      # if hit chance not equal onHit chance roll if additional applications happen
      if applications != chance and random.random() <= chance - applications:
        # print('{} added by chance'.format(ailment))
        applications += 1
      # one bleed for each application
      for i in range(applications):
        durations_.add(ailment, skillAttributes_ = self.skillAttributes)

    # pass damage, next attack speed as well as possibly modified durations (applied ailments and buffs)
    return 0, 0, durations_

  def getAttacktime(self, stats_ = None, tempStats_ = None):
    return 0

# Sentinel AxeThrower attack
class AxeThrower():

  def __init__(self):
    # print('AxeThrower')
    self.attacktimes = [0.]
    self.nAttacktimes = len(self.attacktimes)
    # local skill specific stats for each of the free attacks

    self.skillAttributes = ['strength', 'dexterity']

    self.stats = [stats.Stats() for i in range(3)]

    self.sequence = cycle([0])

    # stores current position in sequence
    self.n = next(self.sequence)

    pass

  def attack(self, durations_, stats_ = None, tempStats_ = None):

    onCooldown = durations_.countActive(type = 'cooldown', sparse = False)['sentinelAxeThrower']
    # no procc if still on cooldown
    if onCooldown:
      # print("onCooldown")
      return 0, 0, durations_

    for ailment, info in stats_.duration.items():

      # add skill specific chances, i.e., ignite chance for rive if skilled
      chance = info['onHit'] + self.stats[self.n].duration[ailment]['onHit']

      if chance == 0:
        continue

      # guaranteed applications
      applications = floor(chance)

      # if hit chance not equal onHit chance roll if additional applications happen
      if applications != chance and random.random() <= chance - applications:
        # print('{} added by chance'.format(ailment))
        applications += 1
      # one bleed for each application
      for i in range(applications):
        durations_.add(ailment, skillAttributes_ = self.skillAttributes)

    # add cooldown duration
    durations_.add('sentinelAxeThrower')

    # pass damage, next attack speed as well as possibly modified durations (applied ailments and buffs)
    return 0, 0, durations_

  def getAttacktime(self, stats_ = None, tempStats_ = None):
    return 0

# Undisputed buff proccing
class Undisputed():

  def __init__(self):
    # print('Undisputed')
    self.attacktimes = [0.]
    self.nAttacktimes = len(self.attacktimes)
    # local skill specific stats for each of the free attacks

    self.skillAttributes = []

    self.stats = [stats.Stats() for i in range(3)]

    self.sequence = cycle([0])

    # stores current position in sequence
    self.n = next(self.sequence)

    pass

  def attack(self, durations_, stats_ = None, tempStats_ = None):

    # add a undisputed buff if a bleeding enemy was hit
    nBleeds = durations_.countActive(type = 'damagingAilment', sparse = False)['bleed']
    if nBleeds >= 1:
      # apply stacks for each enemy
      for i in range(enemies):
        durations_.add('undisputed')

    # pass damage, next attack speed as well as possibly modified durations (applied ailments and buffs)
    return 0, 0, durations_

  def getAttacktime(self, stats_ = None, tempStats_ = None):
    return 0


# A very Generic default Attack providing a possible generic interface
class Default():

  def __init__(self):

    self.attacktimes = [0.68182]
    self.nAttacktimes = len(self.attacktimes)
    # local skill specific stats for each of the free attacks
    self.stats = [stats.Stats() for i in range(self.nAttacktimes)]

    self.skillAttributes = []

    # next(self.sequence) returns following attack
    self.sequence = cycle([0])

    # stores current position in sequence
    self.n = next(self.sequence)
    pass


  # attack, returns next attack time (currently default)
  # todo: possible refactor and put ailment application and strike procs into general skill-independent class-functions
  def attack(self, durations_, stats_ = None, tempStats_ = None):

    # todo: make stat additive and simplify loop only over relevant entries instead of continue
    # for ailment, info in filter(lambda a: a[1]['onHit'] != 0, stats_.duration.items()):

    for ailment, info in stats_.duration.items():

      # add skill specific chances, i.e., ignite chance for rive if skilled
      chance = info['onHit'] + self.stats[self.n].duration[ailment]['onHit']

      if chance == 0:
        continue

      # guaranteed applications
      applications = floor(chance)

      # if hit chance not equal onHit chance roll if additional applications happen
      if applications != chance and random.random() <= chance - applications:
        # print('{} added by chance'.format(ailment))
        applications += 1
      # one bleed for each application
      for i in range(applications):
        durations_.add(ailment, skillAttributes_ = self.skillAttributes)

    # update sequence position after hit
    self.n = next(self.sequence)

    # procs like manifest strike
    for proc, info in stats_.proc.items():
      # add skill specific chances, i.e., ignite chance for rive if skilled
      chance = info['onHit'] + self.stats[self.n].proc[proc]['onHit']

      # guaranteed applications
      applications = floor(chance)

      # if hit chance not equal onHit chance roll if additional applications happen
      if applications != chance and random.random() <= chance - applications:
        # print('{} added by chance'.format(ailment))
        applications += 1
      for i in range(applications):
        # eval(proc) calls constructor of relevant attack
        # todo: maybe pass stats and others as well
        _, attacktime, durations_ = eval(proc)().attack(durations_, stats_)
        # _, attacktime, durations_ = ManifestStrike().attack(durations_, stats_)


    # pass damage, next attack speed as well as possibly modified durations (applied ailments and buffs)
    return 0, self.getAttacktime(stats_, tempStats_), durations_

  def getAttacktime(self, stats_ = None, tempStats_ = None):

    if stats_ != None:
      return self.attacktimes[self.n] / (1 + stats_.increase['meleeAttackSpeed'] + self.stats[self.n].increase['meleeAttackSpeed']) / (stats_.more['meleeAttackSpeed'] * self.stats[self.n].more['meleeAttackSpeed'])
    else:
      return self.attacktimes[self.n]

