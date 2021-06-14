from itertools import cycle
from math import floor
import sys
import random
random.seed()
sys.path.append("..")
import stats
import duration
import data

# generic work in progress enemy counter; scales some buff creations linearly
# assuming debuffs are the same on all enemies
enemies = 1
print("enemies: " + str(enemies))

# generic attack class providing an interface for specific attacks
# as well as implementations for generics like buff/debuff applications and trigger effects
class Default():

  # attack constructor; expects array of attack times (supporting cycling skills), a pattern which describes
  # how the skill loops through its parts as well as skill specific attributes for scaling
  def __init__(self, attacktimes_ = [0.68182], pattern_ = None, attributes_ = []):

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

    # skill scaling attribute
    self._attributes = attributes_

    # attack specific cooldown in seconds
    self._skillCooldown = 0

    # dict of skill specific talents as tuple with information about current and max points, i.e., (cadence, 0, 1) for inactive cadence for Rive
    self._talents = {}

    # flag which tells if talent updates have been prepared
    self._prepared = False

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
      # _globalSkillStats should have properties for stats effecting all damage; must be returned
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
      print('{}: {}'.format(key, value))
      if key in self._talents.keys():
        if value > self._talents[key][1] or value < 0:
          print('Warning: Value "{}" not supported for talent "{}" of "{}". Set to "{}" instead.'.format(value, key,  self._skillName, self._talents[key][1]))
          self._talents[key][0] = self._talents[key][1]
        else:
          self._talents[key][0] = value
      else:
        print('Warning: Talent with name "{}" is not available for "{}". Skipped.'.format(key,self._skillName))
        continue
      pass
    self._prepared = False
    pass

  # empty duration container if no durations are passed, but regularly this should always be provided
  # todo: make it a necessity after testing
  # todo: change order of duration and stats later to match class implementations
  def attack(self, durations_ = duration.Durations(), stats_ = stats.Stats()):

    self.prepare()

    # executes skill only if not on cooldown
    if not self.onCooldown(durations_):

      _damage = 0

      _skillDamage = self.skillHit(stats_, durations_)

      _durations = self.skillEffect(stats_, durations_)

      _durations = self.applyOnHit(stats_, _durations)

      _triggerDamage, _durations = self.onHitTrigger(stats_, _durations)

      # prepare next attack
      self._n = next(self._patternCycle)

      _durations = self.applyCooldown(_durations)

      # return everything which has to be passed to character: damage, (new) durations, (next attack time,)
      return _damage, self.getAttacktime(stats_), _durations

    else:
      # print(self._skillName + " is still on cooldown")
      return 0, self.getAttacktime(stats_), durations_

  # skill specific hit which should be overriden by skill-Implementations
  def skillHit(self, stats_, durations_):

    _damage = 0

    # print("defaultSkillHit")

    return _damage

  # calculates on hit chance for 'ailment_'
  # generic implementation; should only rarely be changed by implemented skills
  def getOnHitChance(self, ailment_, stats_):

    # print("defaultAilmentChance")
    # ailment chance on hit only
    chance = stats_.duration[ailment_]['onHit'] \
            + self._localSkillStats[self._n].duration[ailment_]['onHit']

    return chance

  # applies onHit effects
  # generic implementation; must not be changed by implemented skills
  def applyOnHit(self, stats_, durations_):

    # get all damagingAilments and shreds
    for ailment, ailmentInfo in data.getDurationData('damagingAilment', 'shred', 'buff').items():
      chance = self.getOnHitChance(ailment, stats_)

      if chance == 0:
        continue

      # when a conidtion os provided test if the requirement is full-filled, i.e., if a buff/debuff is applied
      if ailmentInfo['condition'] != None and ailmentInfo['condition'] not in durations_.countActive():
        continue


      # guaranteed applications
      applications = floor(chance)

      # if hit chance not equal onHit chance roll if additional applications happen
      if applications != chance and random.random() <= chance - applications:
        # print('{} added by chance'.format(ailment))
        applications += 1
      # one bleed for each application
      for i in range(applications):
        durations_.add(ailment, skillAttributes_ = self._attributes)

      # print('Ailment: {}, chance: {}'.format(ailment, chance))

    return durations_

  # skill specific proc stuff which should be overriden by skill-Implementations
  def skillEffect(self, stats_, durations_):

    # print("defaultSkillEffect")

    return durations_

  # calculates trigger chance for 'trigger_'
  # generic implementation; should only rarely be changed by implemented skills
  def getTriggerChance(self, trigger_, stats_):

    # print("defaultTriggerChance")
    # trigger chance on hit only
    chance = stats_.proc[trigger_]['onHit'] \
            + self._localSkillStats[self._n].proc[trigger_]['onHit']

    return chance

  # triggers trigger effects
  # generic implementation; must not be changed by implemented skills
  def onHitTrigger(self, stats_, durations_):

    _damage = 0

    for trigger in data.getTrigger():
      chance = self.getTriggerChance(trigger, stats_)

      if chance == 0:
        continue

      # print('Trigger: {}, chance: {}'.format(trigger, chance))

      # guaranteed applications
      applications = floor(chance)

      # if hit chance not equal onHit chance roll if additional applications happen
      if applications != chance and random.random() <= chance - applications:
        applications += 1
      for i in range(applications):
        # triggers skill; eval(proc) calls constructor of relevant attack
        # return damage, irrelevant attacktime (beacuse trigger are instant), and modified durations_
        damage, _, durations_ = eval(trigger)().attack(durations_, stats_)
        _damage += damage
        # _, attacktime, durations_ = ManifestStrike().attack(durations_, stats_)

    return _damage, durations_

  # tests if skill is on cooldown
  # generic implementation; must not be changed by implemented skills
  def onCooldown(self, durations_):
    if self._skillCooldown == 0:
      return 0
    else:
      return (1 if self._skillName in durations_.countActive(type = 'cooldown') else 0)

  # applies skill specific cooldown
  # generic implementation; must not be changed by implemented skills
  def applyCooldown(self, durations_):

    if self._skillCooldown != 0:
      durations_.add(self._skillName, duration_ = self._skillCooldown)

    return durations_

  # returns attacktime of next attack
  # generic implementation; must not be changed by implemented skills
  # todo: add stats per global add from Character/Environment or just pass it always?
  def getAttacktime(self, stats_ = stats.Stats()): # , stats_ = None, tempStats_ = None):
    self.prepare()
    return self._attacktimes[self._n] / (1 + stats_.increase['meleeAttackSpeed'] + self._localSkillStats[self._n].increase['meleeAttackSpeed']) / (stats_.more['meleeAttackSpeed'] * self._localSkillStats[self._n].more['meleeAttackSpeed'])

# default melee attack class
class Melee(Default):
  def __init__(self, attacktimes_ = [0.68182], pattern_ = [0], attributes_ = []):
    super().__init__(attacktimes_, pattern_, attributes_)

    # skillname
    self._skillName = 'Melee'

    pass

  def getOnHitChance(self, ailment_, stats_):

    # print("meleeAilmentChance")
    # ailment chance on hit and melee hit
    chance = stats_.duration[ailment_]['onHit'] \
            + stats_.duration[ailment_]['onMeleeHit'] \
            + self._localSkillStats[self._n].duration[ailment_]['onHit'] \
            + self._localSkillStats[self._n].duration[ailment_]['onMeleeHit']

    return chance

  def getTriggerChance(self, trigger_, stats_):

    # print("meleeTriggerChance")
    # ailment chance on hit and melee hit
    chance = stats_.proc[trigger_]['onHit'] \
            + stats_.proc[trigger_]['onMeleeHit'] \
            + self._localSkillStats[self._n].proc[trigger_]['onHit'] \
            + self._localSkillStats[self._n].proc[trigger_]['onMeleeHit']

    return chance

# default spell attack class
class Spell(Default):
  def __init__(self, attacktimes_ = [0.68182], pattern_ = [0], attributes_ = []):
    super().__init__(attacktimes_, pattern_, attributes_)

    # skillname
    self._skillName = 'Spell'

    pass

  def getOnHitChance(self, ailment_, stats_):

    # print("spellAilmentChance")
    # ailment chance on hit and spell hit
    chance = stats_.duration[ailment_]['onHit'] \
            + stats_.duration[ailment_]['onSpellHit'] \
            + self._localSkillStats[self._n].duration[ailment_]['onHit'] \
            + self._localSkillStats[self._n].duration[ailment_]['onSpellHit']

    return chance

  def getTriggerChance(self, trigger_, stats_):

    # print("spellTriggerChance")
    # ailment chance on hit and spell hit
    chance = stats_.proc[trigger_]['onHit'] \
            + stats_.proc[trigger_]['onSpellHit'] \
            + self._localSkillStats[self._n].proc[trigger_]['onHit'] \
            + self._localSkillStats[self._n].proc[trigger_]['onSpellHit']

    return chance

# default throw attack class
class Throw(Default):
  def __init__(self, attacktimes_ = [0.68182], pattern_ = [0], attributes_ = []):
    super().__init__(attacktimes_, pattern_, attributes_)

    # skillname
    self._skillName = 'Throw'

    pass

  def getOnHitChance(self, ailment_, stats_):

    # print("throwAilmentChance")
    # ailment chance on hit and throw hit
    chance = stats_.duration[ailment_]['onHit'] \
            + stats_.duration[ailment_]['onThrowHit'] \
            + self._localSkillStats[self._n].duration[ailment_]['onHit'] \
            + self._localSkillStats[self._n].duration[ailment_]['onThrowHit']

    return chance

  def getTriggerChance(self, trigger_, stats_):

    # print("throwTriggerChance")
    # ailment chance on hit and throw hit
    chance = stats_.proc[trigger_]['onHit'] \
            + stats_.proc[trigger_]['onThrowHit'] \
            + self._localSkillStats[self._n].proc[trigger_]['onHit'] \
            + self._localSkillStats[self._n].proc[trigger_]['onThrowHit']

    return chance

# Rive
class Rive(Melee):

  def __init__(self, attacktimes_ = [0.68182, 0.68182, 0.68182], pattern_ = [0, 1, 2], attributes_ = ['strength']):
    super().__init__(attacktimes_, pattern_, attributes_)

    # skillname
    self._skillName = 'Rive'

    # available and supported talents
    self._talents = {'cadence' : [0,1], 'flurry' : [0,5], 'sever' : [0,3], 'twistingFangs' : [0,3], 'execution' : [0,1], 'indomitable' : [0,1]}

    pass

  def prepareSkill(self):
    # print("RivePrepare")

    # reinitialize local skillStats
    self._localSkillStats = [stats.Stats() for i in range(self._nAttacks)]

    # flurry: increased melee attack for first and second hit
    self._localSkillStats[0].increase['meleeAttackSpeed'] += 0.08 * self._talents['flurry'][0]
    self._localSkillStats[1].increase['meleeAttackSpeed'] += 0.08 * self._talents['flurry'][0]

    # sever: ignite chance for first hit
    self._localSkillStats[0].duration['ignite']['onHit'] += 0.5 * self._talents['sever'][0]

    # twistingFangs: ignite chance for second hit
    self._localSkillStats[1].duration['ignite']['onHit'] += 0.5 * self._talents['twistingFangs'][0]

    # cadence: changes pattern to [0,1,0,1,2] instead of [0,1,2]
    if self._talents['cadence'][0] == 1:
      self._pattern = [0,1,0,1,2]

    self._localSkillStats[0].proc['RiveIndomitable']['onMeleeHit'] += 1. * self._talents['indomitable'][0]

    pass

  # skill specific hit which should be overriden by skill-Implementations
  def skillHit(self, stats_, durations_):

    _damage = 0

    # print("riveSkillHit")

    return _damage

  # skill specific proc stuff
  def skillEffect(self, stats_, durations_):

    # print("riveSkillEffect")
    # execution: add buff per removed ignite stack
    if self._talents['execution'][0] == 1:
      # number of active ignites; currently multiplied by number of enemies assuming equally applied ignite stacks
      nDamagingAilments = durations_.countActive(type = 'damagingAilment')
      nIgnites = (nDamagingAilments['ignite'] if 'ignite' in nDamagingAilments else 0) * enemies
      # removes all ignite debuffs and adds equal number of riveExecution buffs
      durations_.damagingAilments[:] = [a for a in durations_.damagingAilments if a.getName() != 'ignite']
      for i in range(nIgnites):
        durations_.add('riveExecution')

    return durations_


# Warpath
class Warpath(Melee):
  def __init__(self, attacktimes_ = [0], pattern_ = [0], attributes_ = ['strength']):
      super().__init__(attacktimes_, pattern_, attributes_)

      self._skillName = "Warpath"

  # warpath overloads ailmentChance as it is reduced by 40%
  def getOnHitChance(self, ailment_, stats_):
    # todo: only for ailments, i.e., currently shred and ailments
    return super().getOnHitChance(ailment_, stats_) * 0.6



# trigger calls overrides trigger chance as it cannot procc anything else? or only not itself again?
# but it can still apply ailments
class Trigger():
  def getTriggerChance(self, trigger_, stats_):
    return 0



# Manifest Strike trigger
class ManifestStrike(Trigger, Melee):
  # todo: attribute scaling?
  def __init__(self, attacktimes_ = [0], pattern_ = [0], attributes_ = []):
      super().__init__(attacktimes_, pattern_, attributes_)

      self._skillName = "ManifestStrike"

  # skill specific hit which should be overriden by skill-Implementations
  def skillHit(self, stats_, durations_):

    _damage = 0

    # print("manifestStrikeSkillHit")

    return _damage

# SentinelAxeThrower trigger
class SentinelAxeThrower(Trigger, Melee):
  def __init__(self, attacktimes_ = [0], pattern_ = [0], attributes_ = ['strength', 'dexterity']):
      super().__init__(attacktimes_, pattern_, attributes_)

      self._skillName = "SentinelAxeThrower"
      self._skillCooldown = 1

  # skill specific hit which should be overriden by skill-Implementations
  def skillHit(self, stats_, durations_):

    _damage = 0

    # print("sentinelAxeThrowerSkillHit")

    return _damage

# Rive Indomitable trigger
class RiveIndomitable(Trigger, Spell):
  def __init__(self, attacktimes_ = [0], pattern_ = [0], attributes_ = ['strength']):
      super().__init__(attacktimes_, pattern_, attributes_)

      self._skillName = "RiveIndomitable"

  # skill specific hit which should be overriden by skill-Implementations
  def skillHit(self, stats_, durations_):

    _damage = 0

    # print("riveIndomitableSkillHit")

    return _damage    