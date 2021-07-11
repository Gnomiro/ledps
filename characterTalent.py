import modifier

import warnings

verbosity = 0

class TalentBase:
  """docstring for TalentBase"""

  def __init__(self, name_, points_):
    self._name = name_
    self._points = points_
    self._modifier = modifier.Modifier()

  def getModifier(self):
    return self._modifier


class TalentNotImplemented(TalentBase):
  """docstring for TalentNotImplemented"""

  def __init__(self, name_):
    super(TalentNotImplemented, self).__init__(name_, 0)
    warnings.warn('{} not implemented yet.'.format(self._name))


class SentinelJuggernaut(TalentBase):
  """docstring for SentinelJuggernaut"""

  def __init__(self, points_):
    super(SentinelJuggernaut, self).__init__(name_ = 'sentinelJuggernaut', points_ = points_)
    self._modifier.addAttribute('strength', points_)


class SentinelBlademaster(TalentBase):
  """docstring for SentinelBlademaster"""

  def __init__(self, points_):
    super(SentinelBlademaster, self).__init__(name_ = 'SentinelBlademaster', points_ = points_)
    self._modifier.addIncrease('meleeAttackSpeed', 0.06 * points_)


class SentinelAxeThrower(TalentBase):
  """docstring for SentinelAxeThrower"""

  def __init__(self, points_):
    super(SentinelAxeThrower, self).__init__(name_ = 'sentinelAxeThrower', points_ = points_)
    self._modifier.addTrigger('sentinelAxeThrower', 'onHit', 0.08 * points_)


class PaladinPenance(TalentBase):
  """docstring for PaladinPenance"""

  def __init__(self, points_):
    super(PaladinPenance, self).__init__(name_ = 'paladinPenance', points_ = points_)
    self._modifier.addDuration('bleed', 'onMeleeHit', 0.2 * points_)
    self._modifier.addDuration('bleed', 'onThrowHit', 0.2 * points_)


class PaladinConviction(TalentBase):
  """docstring for PaladinConviction"""

  def __init__(self, points_):
    super(PaladinConviction, self).__init__(name_ = 'paladinConviction', points_ = points_)
    self._modifier.addIncrease('physical', 0.04 * points_)
    self._modifier.addPenetration('physical', 0.02 * points_)
    self._modifier.addIncrease('fire', 0.04 * points_)
    self._modifier.addPenetration('fire', 0.02 * points_)


class PaladinDivineBolt(TalentBase):
  """docstring for PaladinDivineBolt"""

  def __init__(self, points_):
    super(PaladinDivineBolt, self).__init__(name_ = 'paladinDivineBolt', points_ = points_)
    self._modifier.addTrigger('divineBolt', 'onMeleeHit', 0.2 * points_)


class PaladinRedemption(TalentBase):
  """docstring for PaladinRedemption"""

  def __init__(self, points_):
    super(PaladinRedemption, self).__init__(name_ = 'paladinRedemption', points_ = points_)
    self._modifier.addDuration('bleed', 'effect', 0.07 * points_)
    warnings.warn('\'{}\' conditionals are disabled.'.format(self._name))


class PaladinReverenceOfDuality(TalentBase):
  """docstring for PaladinReverenceOfDuality"""

  def __init__(self, points_):
    super(PaladinReverenceOfDuality, self).__init__(name_ = 'paladinReverenceOfDuality', points_ = points_)
    self._modifier.addIncrease('generic', 0.02 * points_)


class BeastmasterUrsineStrength(TalentBase):
  """docstring for BeastmasterUrsineStrength"""

  def __init__(self, points_):
    super(BeastmasterUrsineStrength, self).__init__(name_ = 'beastmasterUrsineStrength', points_ = points_)
    self._modifier.addAttribute('strength', points_)


class Talent:
  """docstring for Talent"""

  def __init__(self, name_, points_):
    talentName = name_[0].upper() + name_[1:]
    try:
      self._talent = eval(talentName)(points_ = points_)
    except NameError:
      self._talent = TalentNotImplemented(talentName)

  def getModifier(self):
    return self._talent.getModifier()