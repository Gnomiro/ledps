import random
random.seed()
from itertools import cycle
from math import floor

from damage import Damage

import stats, duration, data

# generic work in progress enemy counter; scales some buff creations linearly
# assuming debuffs are the same on all enemies
enemies = 1
print("enemies: " + str(enemies))


#########################################################################################################
# Generic base skills
#########################################################################################################


# generic attack class providing an interface for specific attacks
# as well as implementations for generics like buff/debuff applications and trigger effects
class Default():

  # attack constructor; expects array of attack times (supporting cycling skills), a pattern which describes
  # todo: gearStats must only be equipment later
  def __init__(self, attacktimes_ = [0.68182], pattern_ = None, gearStats_ = stats.Stats()):

    # skillname
    self._skillName = 'Default'

    # attacktimes list; supports multiple times for multi-attack skills
    self._attacktimes = attacktimes_
    # number of different attacks
    self._nAttacks = len(self._attacktimes)

    # attack-pattern for multi-attack skills
    self._pattern = pattern_
    if pattern_ == None:
      # default pattern loops through all attacks
      self._pattern = range(len(attacktimes_))

    # attack specific cooldown in seconds
    self._skillCooldown = 0

    # dict of skill specific talents as tuple with information about current and max points, i.e., (cadence, 0, 1) for inactive cadence for Rive
    self._talents = {}

    # flag which tells if talent updates have been prepared
    self._prepared = True

    # stat scaling through attributes
    self._gearStats = gearStats_
    self._attrributeStats = stats.Stats()

    # _localSkillStats should have properties for stats effecting skill damage only
    self._localSkillStats = [stats.Stats() for i in range(self._nAttacks)]
    # _globalSkillStats should have properties for stats effecting all damage; todo: must be returned or applied as buff
    self._globalSkillStats = stats.Stats()
    # initial loop position
    self._patternCycle = cycle(self._pattern)
    self._n = next(self._patternCycle)

    pass

  # prepare skill and set boolean
  # called for all specific implementations; calculates stats provided by skill based on talent selection
  # recalculates if some talents has been changed since lst attack
  # generic implementation; must not be changed by implemented skills
  def prepare(self):

    if not self._prepared:
      # reset skill specific stats
      # do I need both?
      # _localSkillStats should have properties for stats effecting skill damage only
      self._localSkillStats = [stats.Stats() for i in range(self._nAttacks)]
      # _globalSkillStats should have properties for stats effecting all damage; todo: must be returned or applied as buff
      self._globalSkillStats = stats.Stats()
      self.prepareSkill()
      # initial loop position
      self._patternCycle = cycle(self._pattern)
      self._n = next(self._patternCycle)
      self._prepared = True

    pass

  # update stats object according to talents
  # must be provided by skill implementation
  def prepareSkill(self):
    pass

  # set Talents and set prepared to False
  # generic implementation; must not be changed by implemented skills
  def setTalent(self, **talents_):
    for key, value in talents_.items():
      # cast input: uncapitalize key, cast value to integer
      key, value = key[0].lower() + key[1:], int(value)
      if key in self._talents.keys():
        if value > self._talents[key][1] or value < 0:
          print('Warning: Value "{}" not supported for talent "{}" of "{}". Set to "{}" instead.'.format(value, key,  self._skillName, self._talents[key][1]))
          self._talents[key][0] = self._talents[key][1]
        else:
          self._talents[key][0] = value
      else:
        print('Warning: Talent with name "{}" is not available for "{}". Skipped.'.format(key,self._skillName))
        continue
      print('{}: {}'.format(key, self._talents[key][0]))
      self._prepared = False
    pass

  # empty duration container if no durations are passed, but regularly this should always be provided
  def attack(self, durations_ = duration.Durations(), tmpStats_ = stats.Stats()):

    self.prepare()

    # executes skill only if not on cooldown
    if not self.onCooldown(durations_):

      # attack specific stats composed from current tmpStats (including buffs), localSkillStats as well as attribute scaling)
      tmpStats = tmpStats_ + self._localSkillStats[self._n]
      tmpAndAttrStats = tmpStats + self._attrributeStats
      # print(tmpStats)

      skillDamage = self.skillHit(tmpAndAttrStats, durations_)

      durations = self.skillEffect(tmpAndAttrStats, durations_)

      durations = self.applyOnHit(tmpAndAttrStats, durations)

      # trigger does not get attribute stats passed
      triggerDamage, durations = self.onHitTrigger(tmpStats, durations)

      # prepare next attack
      self._n = next(self._patternCycle)

      durations = self.applyCooldown(durations)

      # return everything which has to be passed to character: damage, (new) durations, (next attack time,)
      return (skillDamage + triggerDamage), self.getAttacktime(tmpStats), durations

    else:
      # print(self._skillName + " is still on cooldown")
      return Damage(), self.getAttacktime(tmpStats_), durations_

  # skill specific hit which should be overriden by skill-Implementations
  def skillHit(self, tmpStats_, durations_):

    damage = Damage()

    # print("defaultSkillHit")

    return damage

  # calculates on hit chance for 'name_'
  # generic implementation; should only rarely be changed by implemented skills
  def getOnHitChance(self, name_, stats_):

    # print("defaultOnHitChance")
    # onHit chance for all generic hits only
    chance = stats_.getDurationModifier(name_, 'onHit')

    return chance

  # applies onHit effects
  # generic implementation; must not be changed by implemented skills
  def applyOnHit(self, stats_, durations_):

    # get all damagingAilments, shreds and buffs
    for name, info in data.getDurationData('damagingAilment', 'shred', 'buff').items():
      chance = self.getOnHitChance(name, stats_)

      if chance == 0:
        continue

      if not all([self.evaluateCondition(durations_, ct, c) for ct, c in data.getDurationData()[name]['condition'].items()]):
        print('Warning: Conditions not met!')
        return durations_

      # guaranteed applications
      applications = floor(chance)

      # if hit chance not equal onHit chance roll if additional applications happen
      if applications != chance and random.random() <= chance - applications:
        # print('{} added by chance'.format(name))
        applications += 1
      # one bleed for each application
      for i in range(applications):
        durations_.add(name, tmpStats_ = stats_)

      # print('Duration: {}, chance: {}'.format(name, chance))

    return durations_


  def evaluateCondition(self, durations_, conditionType_, condition_):
    if conditionType_ == 'isActive':
      return durations_.countActiveByNames(condition_)[condition_] != 0
    else:
      print('Warning: Condition-type not yet supported!')
      return False
    pass

  # skill specific proc stuff which should be overriden by skill-Implementations
  def skillEffect(self, stats_, durations_):

    # print("defaultSkillEffect")

    return durations_

  # calculates trigger chance for 'trigger_'
  # generic implementation; should only rarely be changed by implemented skills
  def getTriggerChance(self, trigger_, stats_):

    # print("defaultTriggerChance")
    # trigger chance on hit only
    chance = stats_.getTriggerModifier(trigger_, 'onHit')

    return chance

  # triggers trigger effects
  # generic implementation; must not be changed by implemented skills
  def onHitTrigger(self, stats_, durations_):

    damage = Damage()

    for trigger, info in data.getSupportedTriggerData().items():
      chance = self.getTriggerChance(trigger, stats_) * info['onHitEffectiveness']

      if chance == 0:
        continue

      # print('Trigger: {}, chance: {}'.format(trigger, chance))

      # guaranteed applications
      applications = floor(chance)

      # if hit chance not equal onHit chance roll if additional applications happen
      if applications != chance and random.random() <= chance - applications:
        applications += 1
      for i in range(applications):
        # print('{} chance: {}, info: {}'.format(trigger, chance, data.getSupportedTriggers()[trigger]))
        # triggers skill; eval(proc) calls constructor of relevant attack
        # return damage, irrelevant attacktime (beacuse trigger are instant), and modified durations_
        # info['onTriggerExecutions'] tells how many projectiles/executions happen which can hit the same target
        for _ in range(info['onTriggerExecutions']):
          triggerDamage, _, durations_ = eval(trigger)(gearStats_ = self._gearStats).attack(durations_, stats_)
          damage += triggerDamage

    return damage, durations_

  # tests if skill is on cooldown
  # generic implementation; must not be changed by implemented skills
  def onCooldown(self, durations_):
    if self._skillCooldown == 0:
      return 0
    else:
      return durations_.countActiveByNames(self._skillName)[self._skillName]

  # applies skill specific cooldown
  # generic implementation; must not be changed by implemented skills
  def applyCooldown(self, durations_):

    if self._skillCooldown != 0:
      durations_.add(self._skillName, duration_ = self._skillCooldown, type_ = 'cooldown')

    return durations_

  # returns attacktime of next attack
  # generic implementation; must not be changed by implemented skills
  def getAttacktime(self, stats_ = stats.Stats()):
    self.prepare()
    return self._attacktimes[self._n] / (1. + stats_.getIncrease('meleeAttackSpeed')) / stats_.getMore('meleeAttackSpeed')

# generic melee attack class
class Melee(Default):
  def __init__(self, attacktimes_ = [0.68182], pattern_ = None, gearStats_ = stats.Stats()):
    super().__init__(attacktimes_ = attacktimes_, pattern_ = pattern_, gearStats_= gearStats_)

    # skillname
    self._skillName = 'Melee'

    pass

  def getOnHitChance(self, name_, stats_):

    # print("meleeOnHitChance")
    # onHit chance for generic hit and melee hit
    chance = stats_.getDurationModifier(name_,'onHit') \
            + stats_.getDurationModifier(name_,'onMeleeHit')

    return chance

  def getTriggerChance(self, trigger_, stats_):

    # print("meleeTriggerChance")
    # onHit chance for generic hit and melee hit
    chance = stats_.getTriggerModifier(trigger_, 'onHit') \
            + stats_.getTriggerModifier(trigger_, 'onMeleeHit')

    return chance

# generic spell attack class
class Spell(Default):
  def __init__(self, attacktimes_ = [0.68182], pattern_ = None, gearStats_ = stats.Stats()):
    super().__init__(attacktimes_ = attacktimes_, pattern_ = pattern_, gearStats_= gearStats_)

    # skillname
    self._skillName = 'Spell'

    pass

  def getOnHitChance(self, name_, stats_):

    # print("spellOnHitChance")
    # onHit chance generic hit and spell hit
    chance = stats_.getDurationModifier(name_, 'onHit') \
            + stats_.getDurationModifier(name_, 'onSpellHit')

    return chance

  def getTriggerChance(self, trigger_, stats_):

    # print("spellTriggerChance")
    # onHit chance for generic hit and spell hit
    chance = stats_.getTriggerModifier(trigger_, 'onHit') \
            + stats_.getTriggerModifier(trigger_, 'onSpellHit')

    return chance

# generic throw attack class
class Throw(Default):
  def __init__(self, attacktimes_ = [0.68182], pattern_ = None, gearStats_ = stats.Stats()):
    super().__init__(attacktimes_ = attacktimes_, pattern_ = pattern_, gearStats_= gearStats_)

    # skillname
    self._skillName = 'Throw'

    pass

  def getOnHitChance(self, name_, stats_):

    # print("throwOnHitChance")
    # onHit chance for generic hit and throw hit
    chance = stats_.getDurationModifier(name_, 'onHit') \
            + stats_.getDurationModifier(name_, 'onThrowHit')

    return chance

  def getTriggerChance(self, trigger_, stats_):

    # print("throwTriggerChance")
    # onHit chance for generic hit and throw hit
    chance = stats_.getTriggerModifier(trigger_, 'onHit') \
            + stats_.getTriggerModifier(trigger_, 'onThrowHit')

    return chance


#########################################################################################################
# Class Skill implementations
#########################################################################################################

#########################################################################################################
# Sentinel
#########################################################################################################

# Rive
class Rive(Melee):

  def __init__(self, gearStats_):
    super().__init__(attacktimes_ = [0.68182 * 0.75, 0.68182 * 0.75, 0.68182 * 0.93], pattern_ = [0, 1, 2], gearStats_ = gearStats_)

    # skillname
    self._skillName = 'Rive'

    # available and supported talents
    self._talents = {'cadence' : [0,1], 'flurry' : [0,5], 'sever' : [0,3], 'twistingFangs' : [0,3], 'execution' : [0,1], 'indomitable' : [0,1]}

    # generic skill specific damage increase provided by attributes
    self._attrributeStats.addIncrease('generic', 0.04 * gearStats_.getAttribute('strength'))

    pass

  def prepareSkill(self):
    # print("RivePrepare")

    # flurry: increased melee attack for first and second hit
    self._localSkillStats[0].addIncrease('meleeAttackSpeed', 0.08 * self._talents['flurry'][0])
    self._localSkillStats[1].addIncrease('meleeAttackSpeed', 0.08 * self._talents['flurry'][0])

    # sever: ignite chance for first hit
    self._localSkillStats[0].addDurationModifier('ignite', 'onHit', 0.5 * self._talents['sever'][0])

    # twistingFangs: ignite chance for second hit
    self._localSkillStats[1].addDurationModifier('ignite', 'onHit', 0.5 * self._talents['twistingFangs'][0])

    # cadence: changes pattern to [0,1,0,1,2] instead of [0,1,2]
    if self._talents['cadence'][0] == 1:
      self._pattern = [0,1,0,1,2]

    # indomitable: rive spell proc in first hit; onHit as only applied by rive
    self._localSkillStats[0].addTriggerModifier('RiveIndomitable', 'onHit', 1. * self._talents['indomitable'][0])

    pass

  # skill specific hit which should be overriden by skill-Implementations
  def skillHit(self, stats_, durations_):

    damage = Damage()

    # print("riveSkillHit")

    return damage

  # skill specific proc stuff
  def skillEffect(self, stats_, durations_):

    # print("riveSkillEffect")
    # execution: add buff per removed ignite stack
    if self._talents['execution'][0] == 1:
      # number of active ignites; currently multiplied by number of enemies assuming equally applied ignite stacks
      nIgnites = durations_.countActiveByNames('ignite')['ignite'] * enemies
      # removes all ignite debuffs and adds equal number of riveExecution buffs
      durations_._durations['damagingAilment'][:] = [a for a in durations_._durations['damagingAilment'] if a.getName() != 'ignite']
      for i in range(nIgnites):
        durations_.add('riveExecution')

    return durations_

# Warpath
class Warpath(Melee):
  # warpath has doubled attack time; multiplicative order does not matter
  def __init__(self, gearStats_):
    super().__init__(attacktimes_ = [0.68182 / 2.], pattern_ = None, gearStats_ = gearStats_)

    self._skillName = "Warpath"
    # available and supported talents
    # self._talents = {'temporalCascade' : [0,5], 'drainingAssault' : [0,5]}

    # generic skill specific damage increase provided by attributes
    self._attrributeStats.addIncrease('generic', 0.04 * gearStats_.getAttribute('strength'))

    pass

  # warpath overloads OnHitChance as it is reduced by 40%
  def getOnHitChance(self, name_, stats_):
    # todo: only for ailments, i.e., currently shred and ailments
    return super().getOnHitChance(name_, stats_) * 0.6


#########################################################################################################
# Primalist
#########################################################################################################

# Swipe
class Swipe(Melee):

  def __init__(self, gearStats_):
    super().__init__(attacktimes_ = [0.68182], pattern_ = None, gearStats_ = gearStats_)

    # skillname
    self._skillName = 'Swipe'

    # available and supported talents
    self._talents = {'bloodBeast' : [0,5], 'rending' : [0,4], 'aspectOfThePanther' : [0,4], 'felineHunter' : [0,1]}

    # generic skill specific damage increase provided by attributes
    self._attrributeStats.addIncrease('generic', 0.04 * gearStats_.getAttribute('strength'))

    pass

  def prepareSkill(self):
    # print("swipePrepare")

    # reset skill specific duration modification
    # todo: handle this somehow more general
    data.durationData['swipeAspectofThePantherGeneric']['maxStack'] = 1

    # bloodBeast: bleed chance on hit
    self._localSkillStats[0].addDurationModifier('bleed', 'onHit', 0.2 * self._talents['bloodBeast'][0])

    # rending: physShred on hit
    self._localSkillStats[0].addDurationModifier('physicalShred', 'onHit', 0.25 * self._talents['rending'][0])

    # aspectOfThePanther modifies maxStack of aspectOfThePantherGeneric buff
    data.durationData['swipeAspectofThePantherGeneric']['maxStack'] = 2 * self._talents['aspectOfThePanther'][0]

    pass

  # skill specific proc stuff
  def skillEffect(self, stats_, durations_):

    # print("swipeSkillEffect")

    # aspectOfThePanther: add increase generic buff
    if self._talents['aspectOfThePanther'][0] > 0:
      durations_.add('swipeAspectofThePantherGeneric')

    # felineHunter: add generic increased speed buff
    if self._talents['felineHunter'][0] == 1:
      durations_.add('swipeAspectofThePantherSpeed')

    return durations_

# Serpent Strike
class SerpentStrike(Melee):

  def __init__(self, gearStats_):
    super().__init__(attacktimes_ = [0.68182], pattern_ = None, gearStats_ = gearStats_)

    # skillname
    self._skillName = 'SerpentStrike'

    # available and supported talents
    self._talents = {'scorpionStrikes' : [0,5], 'chronoStrike' : [0,5], 'debilitatingPoison' : [0,3], 'nagasaVenom' : [0,6], 'plaguebearer' : [0,4], 'venomousIntent' : [0,1]}

    # generic skill specific damage increase provided by attributes
    self._attrributeStats.addIncrease('generic', 0.04 * gearStats_.getAttribute('strength'))
    self._attrributeStats.addIncrease('generic', 0.04 * gearStats_.getAttribute('dexterity'))
    self._attrributeStats.addDurationModifier('poison', 'onMeleeHit', 0.04 * gearStats_.getAttribute('dexterity'))

    pass

  def prepareSkill(self):
    # print("serpentStrikePrepare")

    # reset skill specific buff data to default
    data.durationData['serpentStrikeOnHit']['effect']['increase']['poison'] = 0.
    data.durationData['serpentStrikeOnHit']['effect']['increase']['overTime'] = 0.

    # generic 140% increase poison chance
    self._localSkillStats[0].addDurationModifier('poison', 'onHit', 1.4)

    # debilitatingPoison: adds blinding poison chance
    self._localSkillStats[0].addDurationModifier('blindingPoison', 'onHit', 0.17 * self._talents['debilitatingPoison'][0])

    # scorpionStrikes and chronoStrike implemented by modifying serpentStrikeOnHit buff
    # scorpionStrikes: global increse poison damage
    data.durationData['serpentStrikeOnHit']['effect']['increase']['poison'] = 0.12 * self._talents['scorpionStrikes'][0]
    # chronoStrike: global increase over time damage
    data.durationData['serpentStrikeOnHit']['effect']['increase']['overTime'] = 0.1 * self._talents['chronoStrike'][0]

    # nagasaVenom: poison chance and duration
    self._localSkillStats[0].addDurationModifier('poison', 'onHit', 0.1 * self._talents['chronoStrike'][0])
    self._localSkillStats[0].addDurationModifier('poison', 'duration', 0.1 * self._talents['chronoStrike'][0])

    # plaguebearer: plague chance on hit
    self._localSkillStats[0].addDurationModifier('plague', 'onHit', 0.25 * self._talents['plaguebearer'][0])

    # venomousIntent: reduced poison duration and some additional poison
    # todo verify how it really works
    self._localSkillStats[0].addDurationModifier('poison', 'duration', -0.35 * self._talents['venomousIntent'][0])
    self._localSkillStats[0].addDurationModifier('poison', 'onMeleeHit', 1. * self._talents['venomousIntent'][0])
    # old: it may triggers a skill but according to mike it is more like an additional poison; trigger which is only applied by Serpent Strike (thus as onHit)
    # self._localSkillStats[0].addTriggerModifier('SerpentStrikePoisonSpit', 'onHit', .25 * self._talents['venomousIntent'][0])

    pass

  # skill specific proc stuff
  def skillEffect(self, stats_, durations_):

    # print("serpentStrikeSkillEffect")

    # scorpionStrikes and/or chronoStrike: add onHitBuffs
    if self._talents['scorpionStrikes'][0] > 0 or self._talents['chronoStrike'][0]:
      durations_.add('serpentStrikeOnHit')

    return durations_

#########################################################################################################
# Trigger skills
#########################################################################################################


# trigger calls overrides trigger chance as it cannot procc anything else? or only not itself again?
# but it can still apply onHitEffects
class Trigger():
  def getTriggerChance(self, trigger_, stats_):
    return 0
  pass

# Manifest Strike trigger
class ManifestStrike(Trigger, Melee):
  # todo: attribute scaling?
  def __init__(self, gearStats_):
    super().__init__(attacktimes_ = [0], pattern_ = None, gearStats_ = gearStats_)

    self._skillName = "ManifestStrike"

    # generic skill specific damage increase provided by attributes
    self._attrributeStats.addIncrease('generic', 0.04 * gearStats_.getAttribute('strength'))
    # todo: is attuenemt scaling really just increase?
    self._attrributeStats.addIncrease('generic', 0.04 * gearStats_.getAttribute('attunement'))

    pass

  # skill specific hit which should be overriden by skill-Implementations
  def skillHit(self, stats_, durations_):

    damage = Damage()

    # print("manifestStrikeSkillHit")

    return damage

# SentinelAxeThrower trigger
class SentinelAxeThrower(Trigger, Throw):
  def __init__(self, gearStats_):
    super().__init__(attacktimes_ = [0], pattern_ = None, gearStats_ = gearStats_)

    self._skillName = "SentinelAxeThrower"
    self._skillCooldown = 1

    # generic skill specific damage increase provided by attributes
    self._attrributeStats.addIncrease('generic', 0.04 * gearStats_.getAttribute('strength'))
    self._attrributeStats.addIncrease('generic', 0.04 * gearStats_.getAttribute('dexterity'))

    pass

  # skill specific hit which should be overriden by skill-Implementations
  def skillHit(self, stats_, durations_):

    damage = Damage()

    # print("sentinelAxeThrowerSkillHit")

    return damage

# Rive Indomitable trigger
class RiveIndomitable(Trigger, Spell):
  def __init__(self, gearStats_):
    super().__init__(attacktimes_ = [0], pattern_ = None, gearStats_ = gearStats_)

    self._skillName = "RiveIndomitable"

    # generic skill specific damage increase provided by attributes
    self._attrributeStats.addIncrease('generic', 0.04 * gearStats_.getAttribute('strength'))

  # skill specific hit which should be overriden by skill-Implementations
  def skillHit(self, stats_, durations_):

    damage = Damage()

    # print("riveIndomitableSkillHit")

    return damage

# Divine Bolt trigger
class DivineBolt(Trigger, Spell):
  def __init__(self, gearStats_):
    super().__init__(attacktimes_ = [0], pattern_ = None, gearStats_ = gearStats_)

    self._skillName = "DivineBolt"

    # generic skill specific damage increase provided by attributes
    self._attrributeStats.addIncrease('generic', 0.04 * gearStats_.getAttribute('attunement'))

  # skill specific hit which should be overriden by skill-Implementations
  def skillHit(self, stats_, durations_):

    damage = Damage()

    # print("riveDivineBoltSkillHit")

    return damage

# # Serpent Strike Poison Spit trigger
# class SerpentStrikePoisonSpit(Trigger, Spell):
#   def __init__(self, gearStats_):
#     super().__init__(attacktimes_ = [0], pattern_ = None, gearStats_ = gearStats_)

#     self._skillName = "SerpentStrikePoisonSpit"

#     self._localSkillStats[0].addDurationModifier('poison', 'onSpellHit', 1.)

#   # skill specific hit which should be overriden by skill-Implementations
#   def skillHit(self, stats_, durations_):

#     damage = Damage()

#     # print("riveDivineBoltSkillHit")

#     return damage