import duration

import stats, damage

import numpy

frametime = 0.1

class Character():

  # init cahracter based on stats
  def __init__(self, stats, skill, verbosity = 0):

    # create character stats object
    self.stats = stats

    self.skill = skill

    # ailment-list
    self.durations = duration.Durations(self.stats, verbosity)

    # verbosity level
    self.verbosity = verbosity

    pass

  def combat(self, endtime = 1000, boss = False):
    attacktime = self.skill.getAttacktime(stats_ = self.stats)
    lastattack = 0.

    t = 0

    # first hit at t = 0
    # second hit after attacktime
    # hits are aligned to next servertick
    # todo: attack speed modifications; probably just use buffs at hit-time to determine speed of next hit and assume it constant

    # damage calculation (tick) is done before hit application
    dmg = damage.Damage()
    ailment_tick_damage = damage.Damage()

    while t <= endtime:

      # calculate and accumulate damage
      if t!= 0:
        ailment_tick_damage += self.durations.tick(frametime, boss)

      # flush damage output every 0.5 s, i.e., 5 serverticks with frametime 0.1s
      # test via modulo operator if t % 0.5 is close to 0 or 0.5
      if any(numpy.isclose([t % 0.5, t % 0.5], [0, 0.5], rtol=0, atol=1e-2, equal_nan=False)):
        if self.verbosity >= 1:
          print("t: {}".format(t))
          print('Overall tick damage: {}\n'.format(ailment_tick_damage))
        dmg += ailment_tick_damage
        ailment_tick_damage = damage.Damage()

      while lastattack <= t:
        lastattack += attacktime
        _, attacktime, self.durations = self.skill.attack(self.durations, self.stats)

      t += frametime

    # flush remaining damage into global counter
    if self.verbosity >= 1:
      print("t: {}".format(t))
      print('Overall tick damage: {}\n'.format(ailment_tick_damage))
    dmg += ailment_tick_damage

    return dmg

  def singleHit(self):

    _, self.durations = self.skill.attack(self.durations, self.stats)

    dmg = damage.Damage()
    ailment_tick_damage = damage.Damage()

    t = 0

    while len(list(self.durations.getAll())) != 0:

      # calculate and accumulate damage
      if t != 0:
        ailment_tick_damage += self.durations.tick(frametime)

      # flush damage output every 0.5 s, i.e., 5 serverticks with frametime 0.1s
      # test via modulo operator if t % 0.5 is close to 0 or 0.5
      if any(numpy.isclose([t % 0.5, t % 0.5], [0, 0.5], rtol=0, atol=1e-2, equal_nan=False)):
        if self.verbosity >= 1:
          print("t: {}".format(t))
          print('Overall tick damage: {}\n'.format(ailment_tick_damage))
        dmg += ailment_tick_damage
        ailment_tick_damage = damage.Damage()

      t += frametime

    # flush remaining damage into global counter
    if self.verbosity >= 1:
      print("t: {}".format(t))
      print('Overall tick damage: {}\n'.format(ailment_tick_damage))
    dmg += ailment_tick_damage

    return dmg

