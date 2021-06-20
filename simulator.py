import duration

import stats

import data

from damage import Damage

import numpy

# global frametime for calculations
frametime = 0.1

#########################################################################################################
# Last Epoch combat simulator
#########################################################################################################

# General simualtor class handling details of character and managing buffs/debuffs as well as simulating combat
class Simulator():

  # init simulation based on gearStats and chosen skill
  def __init__(self, gearStats_, skill_, verbosity_ = 0):

    # gear specific stats
    self._gearStats = gearStats_

    # skill to use
    self._skill = skill_

    # duration objects
    self._durations = duration.Durations(verbosity_)

    # verbosity level
    self._verbosity = verbosity_

    pass

  def combat(self, endtime_ = 1000, boss_ = False):

    # start timer
    t = 0

    # time of last hit
    lastattack = 0.

    # assumptions
    # first hit at t = 0
    attacktime = 0
    # second hit after attacktime
    # hits are aligned to next server-frame
    # and consider buffs present at server-frame time

    # global damage containers
    damage = Damage()
    # ailment damage of frame
    ailmentDamage = Damage()
    # skill damage of frame
    skillDamage = Damage()
    # overall accumulated damage between damage 'flush'
    tickDamage = Damage()

    # time loop
    while t <= endtime_:

      # progress durations to next timeframe
      # shifted by one frametime because first application happens in first loop
      # receive damage from damaging duration objects like damagingAilments
      if t!= 0:
        ailmentDamage = self._durations.tick(frametime, boss_)

      # accumualte effects of active buffs into stat-object
      # considers buff effects provided by gear/talents
      tmpStats = stats.Stats().fromBuffs(self._durations, self._gearStats)

      # add constant gear stats to temporary stats
      tmpStats += self._gearStats

      if self._verbosity >= 3:
        print(tmpStats)

      if self._verbosity >= 2:
        print(self._durations.countActive())

      # reset skill damage
      skillDamage = Damage()
      # accumulate hits happening between previous and current server frame
      while lastattack <= t:
        lastattack += attacktime
        # receive skillHitDamage, new attacktime as well as updated durations (ailments/buffs/etc applied are here)
        skillDamageHit, attacktime, self._durations = self._skill.attack(self._durations, tmpStats)
        # skillDamage of server-frame
        skillDamage += skillDamageHit

      # sum up damage
      frameDamage = skillDamage + ailmentDamage

      # get penetration for all elemt types; normalized to 1
      # todo: consider skill specific penetration somehow; return from attack or maybe calculate penetration already in the skill
      #       ailment penetration should be fine on this level
      penetration = {element: (1. + tmpStats.getPenetration(element)) for element in data.getSupportedElementTypes()}
      # print(penetration)
      # count active shreds and add them to penetration from gear; buff and shred limit is considered at application time
      # += for double shreds like poison with builtInShred and shred
      shreds = self._durations.countActiveByTypes('shred')
      for key in shreds:
        # scale shred by penetration value and reduced boss effect; if poisonBuiltInShred also scale with poison effect
        penetration[data.getDurationData()[key]['element']] += shreds[key] * 0.05 * (0.4 if boss_ else 1.) * (1. if key != 'poisonBuiltInShred' else (1. + tmpStats.getDurationData('poison', 'effect')))
      # print(penetration)

      # scale damage by penetration
      frameDamage.multiplyEachElementSeperately(penetration)

      # flush damage output every 0.5 s, i.e., 5 serverticks with frametime 0.1s
      # test via modulo operator if t % 0.5 is close to 0 or 0.5
      tickDamage += frameDamage
      if any(numpy.isclose([t % 0.5, t % 0.5], [0, 0.5], rtol=0, atol=1e-2, equal_nan=False)):
        if self._verbosity >= 2:
          print("t: {}".format(t))
          print('Overall tick damage: {}\n'.format(tickDamage))
        damage += tickDamage
        tickDamage = Damage()

      t += frametime

    # flush remaining damage into global counter
    if self._verbosity >= 2:
      print("t: {}".format(t))
      print('Overall tick damage: {}\n'.format(tickDamage))
    damage += tickDamage

    if self._verbosity >= 1:
      print('Stats at end of fight:')
      print(tmpStats)
      print('Active durations at end of fight:')
      print(self._durations.countActive())

    return damage

  # update later
  # def singleHit(self):

  #   _, self._durations = self._skill.attack(self._durations, self._gearStats)

  #   dmg = Damage()
  #   ailment_tick_damage = Damage()

  #   t = 0

  #   while len(list(self._durations.getAll())) != 0:

  #     # calculate and accumulate damage
  #     if t != 0:
  #       ailment_tick_damage += self._durations.tick(frametime)

  #     # flush damage output every 0.5 s, i.e., 5 serverticks with frametime 0.1s
  #     # test via modulo operator if t % 0.5 is close to 0 or 0.5
  #     if any(numpy.isclose([t % 0.5, t % 0.5], [0, 0.5], rtol=0, atol=1e-2, equal_nan=False)):
  #       if self._verbosity >= 1:
  #         print("t: {}".format(t))
  #         print('Overall tick damage: {}\n'.format(ailment_tick_damage))
  #       dmg += ailment_tick_damage
  #       ailment_tick_damage = Damage()

  #     t += frametime

  #   # flush remaining damage into global counter
  #   if self._verbosity >= 1:
  #     print("t: {}".format(t))
  #     print('Overall tick damage: {}\n'.format(ailment_tick_damage))
  #   dmg += ailment_tick_damage

  #   return dmg

