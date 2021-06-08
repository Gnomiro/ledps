from itertools import cycle
import sys
sys.path.append("..")
import stats
import duration

# generic attack class
class Default():

  def __init__(self, attacktimes_ = [0.68182], pattern_ = [0], attributes_ = []):

    # attacktimes list; supports multiple times for multi-attack skills
    self._attacktimes = attacktimes_
    # number of different attacks
    self._nAttacktimes = len(self._attacktimes)

    # loop-pattern for multi-attack skills
    if pattern_ == []:
      self._pattern = cycle(range(self._nAttacktimes))
    else:
      self._pattern = cycle(pattern_)

    # initial loop position
    self._n = next(self._pattern)

    # skill scaling attribute
    self._attributes = attributes_

    # do I need both?
    # _localSkillStats should have properties for stats effecting skill damage only
    self._localSkillStats = [stats.Stats() for i in range(self._nAttacktimes)]
    # _globalSkillStats should have properties for stats effecting all damage; must be returned
    self._globalSkillStats = stats.Stats()

    # dict of skill specific talents as tuple with information about current and max points, i.e., (cadence, 0, 1) for inactive cadence for Rive
    self._talents = {}

    # flag which tells if talent updates have been prepared
    self._prepared = False

    pass

  # prepare skill and set boolean
  def prepare(self):

    if not self._prepared:
      self.prepareSkill()
      self._prepared = True

    pass

  # update stats object according to talents; must be provided by skill implementation
  def prepareSkill(self):
    pass

  # set Talents and set prepared to False
  def setTalent(self, **kwargs):
    for key, value in kwargs.items():
      print('{}: {}'.format(key, value))
      pass
    self._prepared = False
    pass

  # empty duration container if no durations are passed, but regularly this should always be provided
  # todo: make it a necessity after testing
  def attack(self, stats_ = stats.Stats(), durations_ = duration.Durations()):

    self.prepare()

    _damage = 0

    _skillDamage = self.skillHit(stats_, durations_)

    _durations = self.applyAilments(stats_, durations_)

    _durations = self.skillEffect(stats_, _durations)

    _triggerDamage, _durations = self.onHitTrigger(stats_, _durations)

    # prepare next attack
    self._n = next(self._pattern)

    return _damage, self.getAttacktime(), _durations # return everything which has to be passed to character: damage, (new) durations, (next attack time,)

  # skill specific hit which should be overriden by skill-Implementations
  def skillHit(self, stats_, durations_):

    _damage = 0

    print("defaultSkillHit")

    return _damage

  # skill specific proc stuff which should be overriden by skill-Implementations

  def skillEffect(self, stats_, durations_):

    print("defaultSkillEffect")

    return durations_

  def applyAilments(self, stats_, durations_):

    print("defaultAilments")

    return durations_

  def onHitTrigger(self, stats_, durations_):

    _damage = 0

    print("defaultTrigger")

    return _damage, durations_

  # add stats per global add from Character/Environment or just pass it alwyas?

  def getAttacktime(self): # , stats_ = None, tempStats_ = None):
    return self._attacktimes[self._n]


# default melee attack class
class Melee(Default):
  def __init__(self, attacktimes_ = [0.68182], pattern_ = [0], attributes_ = []):
    super().__init__(attacktimes_, pattern_, attributes_)
    pass

  def applyAilments(self, stats_, durations_):

    print("attackAilments")

    return durations_

  def onHitTrigger(self, stats_, durations_):

    _damage = 0

    print("attackTrigger")

    return _damage, durations_

# default spell attack class
class Spell(Default):
  def __init__(self, attacktimes_ = [0.68182], pattern_ = [0], attributes_ = []):
    super().__init__(attacktimes_, pattern_, attributes_)
    pass

  def applyAilments(self, stats_, durations_):

    print("spellAilments")

    return durations_

  def onHitTrigger(self, stats_, durations_):

    _damage = 0

    print("spellTrigger")

    return _damage, durations_

# default throw attack class
class Throw(Default):
  def __init__(self, attacktimes_ = [0.68182], pattern_ = [0], attributes_ = []):
    super().__init__(attacktimes_, pattern_, attributes_)
    pass

  def applyAilments(self, stats_, durations_):

    print("throwAilments")

    return durations_

  def onHitTrigger(self, stats_, durations_):

    _damage = 0

    print("throwTrigger")

    return _damage, durations_

# Rive
class Rive(Melee):

  def __init__(self, attacktimes_ = [0.68182, 0.68182, 0.68182], pattern_ = [0, 1, 2], attributes_ = ['strength']):
    super().__init__(attacktimes_, pattern_, attributes_)

    # available and supported talents
    # question: this way setTalent can be generic?!
    self._talents = {'flurry' : (0,5)}

    # update talent values
    self.setTalent()

    pass

  def prepareSkill(self):
    print("RivePrepare")
    pass

  # skill specific hit which should be overriden by skill-Implementations
  def skillHit(self, stats_, durations_):

    _damage = 0

    print("riveSkillHit")

    return _damage

  # skill specific proc stuff which should be overriden by skill-Implementations

  def skillEffect(self, stats_, durations_):

    print("riveSkillEffect")

    return durations_

  pass