import modifier

import warnings

verbosity = 0

############################################################################################
############################################################################################
# Talent bass classes
############################################################################################
############################################################################################

class TalentBase:
  """docstring for TalentBase"""

  def __init__(self, name_, points_):
    self._name = name_
    self._points = points_
    self._modifier = modifier.Modifier()
    pass

  def getModifier(self):
    return self._modifier

  def applyModification(self, collection_):
    pass


class TalentNotImplemented(TalentBase):
  """docstring for TalentNotImplemented"""

  def __init__(self, name_):
    super(TalentNotImplemented, self).__init__(name_, 0)
    warnings.warn('{} not implemented yet.'.format(self._name))
    pass


############################################################################################
############################################################################################
# Sentinel talents
############################################################################################
############################################################################################

class SentinelJuggernaut(TalentBase):
  """docstring for SentinelJuggernaut"""

  def __init__(self, points_):
    super(SentinelJuggernaut, self).__init__(name_ = 'sentinelJuggernaut', points_ = points_)
    self._modifier.addAttribute('strength', points_)
    pass


class SentinelBlademaster(TalentBase):
  """docstring for SentinelBlademaster"""

  def __init__(self, points_):
    super(SentinelBlademaster, self).__init__(name_ = 'SentinelBlademaster', points_ = points_)
    self._modifier.addIncrease('meleeAttackSpeed', 0.06 * points_)
    pass


class SentinelAxeThrower(TalentBase):
  """docstring for SentinelAxeThrower"""

  def __init__(self, points_):
    super(SentinelAxeThrower, self).__init__(name_ = 'sentinelAxeThrower', points_ = points_)
    self._modifier.addTrigger('sentinelAxeThrower', 'onHit', 0.08 * points_)
    pass

############################################################################################
# Paladin talents
############################################################################################

class PaladinPenance(TalentBase):
  """docstring for PaladinPenance"""

  def __init__(self, points_):
    super(PaladinPenance, self).__init__(name_ = 'paladinPenance', points_ = points_)
    self._modifier.addDuration('bleed', 'onMeleeHit', 0.2 * points_)
    self._modifier.addDuration('bleed', 'onThrowHit', 0.2 * points_)
    pass


class PaladinConviction(TalentBase):
  """docstring for PaladinConviction"""

  def __init__(self, points_):
    super(PaladinConviction, self).__init__(name_ = 'paladinConviction', points_ = points_)
    self._modifier.addIncrease('physical', 0.04 * points_)
    self._modifier.addPenetration('physical', 0.02 * points_)
    self._modifier.addIncrease('fire', 0.04 * points_)
    self._modifier.addPenetration('fire', 0.02 * points_)
    pass


class PaladinDivineBolt(TalentBase):
  """docstring for PaladinDivineBolt"""

  def __init__(self, points_):
    super(PaladinDivineBolt, self).__init__(name_ = 'paladinDivineBolt', points_ = points_)
    self._modifier.addTrigger('divineBolt', 'onMeleeHit', 0.2 * points_)
    pass


class PaladinRedemption(TalentBase):
  """docstring for PaladinRedemption"""

  def __init__(self, points_):
    super(PaladinRedemption, self).__init__(name_ = 'paladinRedemption', points_ = points_)
    self._modifier.addDuration('bleed', 'effect', 0.07 * points_)
    warnings.warn('\'{}\' conditionals are disabled.'.format(self._name))
    pass


class PaladinReverenceOfDuality(TalentBase):
  """docstring for PaladinReverenceOfDuality"""

  def __init__(self, points_):
    super(PaladinReverenceOfDuality, self).__init__(name_ = 'paladinReverenceOfDuality', points_ = points_)
    self._modifier.addIncrease('generic', 0.02 * points_)
    pass


############################################################################################
############################################################################################
# Primalist talents
############################################################################################
############################################################################################

class PrimalistPrimalStrength(TalentBase):
  """docstring for PrimalistPrimalStrength"""

  def __init__(self, points_):
    super(PrimalistPrimalStrength, self).__init__(name_ = 'primalistPrimalStrength', points_ = points_)
    self._modifier.addAttribute('strength', points_)
    pass

class PrimalistTempestBond(TalentBase):
  """docstring for PrimalistTempestBond"""

  def __init__(self, points_):
    super(PrimalistTempestBond, self).__init__(name_ = 'primalistTempestBond', points_ = points_)
    self._modifier.addIncrease('physical', 0.04 * points_ * 2)
    self._modifier.addIncrease('cold', 0.04 * points_ * 2)
    self._modifier.addIncrease('lightning', 0.04 * points_ * 2)

    warnings.warn('PrimalistTempestBond assumes minion as active.')
    pass

############################################################################################
# Beastmaster talents
############################################################################################

class BeastmasterUrsineStrength(TalentBase):
  """docstring for BeastmasterUrsineStrength"""

  def __init__(self, points_):
    super(BeastmasterUrsineStrength, self).__init__(name_ = 'beastmasterUrsineStrength', points_ = points_)
    self._modifier.addAttribute('strength', points_)
    pass

class BeastmasterHunterOfTheDeep(TalentBase):
  """docstring for BeastmasterHunterOfTheDeep"""

  def __init__(self, points_):
    super(BeastmasterHunterOfTheDeep, self).__init__(name_ = 'beastmasterHunterOfTheDeep', points_ = points_)
    self._modifier.addDuration('aspectOfTheShark', 'duration', 0.15 * points_)
    pass

class BeastmasterPrimalStrength(TalentBase):
  """docstring for BeastmasterPrimalStrength"""

  def __init__(self, points_):
    super(BeastmasterPrimalStrength, self).__init__(name_ = 'beastmasterPrimalStrength', points_ = points_)
    self._modifier.addAttribute('strength', points_)
    pass

class BeastmasterViperFangs(TalentBase):
  """docstring for BeastmasterViperFangs"""

  def __init__(self, points_):
    super(BeastmasterViperFangs, self).__init__(name_ = 'beastmasterViperFangs', points_ = points_)
    self._modifier.addIncrease('meleeAttackSpeed', points_ * 0.05)
    self._modifier.addDuration('aspectOfTheViper', 'onHit', points_ * 0.03)
    pass

class BeastmasterEnvenom(TalentBase):
  """docstring for BeastmasterEnvenom"""

  def __init__(self, points_):
    super(BeastmasterEnvenom, self).__init__(name_ = 'beastmasterEnvenom', points_ = points_)
    self._modifier.addDuration('poison', 'onMeleeHit', points_ * 0.08)
    pass

class BeastmasterTheCircleOfLife(TalentBase):
  """docstring for BeastmasterTheCircleOfLife"""

  def __init__(self, points_):
    super(BeastmasterTheCircleOfLife, self).__init__(name_ = 'beastmasterTheCircleOfLife', points_ = points_)
    self._modifier.addDuration('aspectOfTheShark', 'onHit', points_ * 0.05)

    warnings.warn('BeastmasterTheCircleOfLife always assumes DragonSlayer active and fight against bosses')
    pass

class BeastmasterOceanMaw(TalentBase):
  """docstring for BeastmasterOceanMaw"""

  def __init__(self, points_):
    super(BeastmasterOceanMaw, self).__init__(name_ = 'beastmasterOceanMaw', points_ = points_)
    self._modifier.addDuration('aspectOfTheShark', 'effect', points_ * 0.15)
    self._modifier.addDuration('aspectOfTheShark', 'duration', points_ * 0.15)
    pass

class BeastmasterFeedingFrenzy(TalentBase):
  """docstring for BeastmasterFeedingFrenzy"""

  def __init__(self, points_):
    super(BeastmasterFeedingFrenzy, self).__init__(name_ = 'beastmasterFeedingFrenzy', points_ = points_)

    self._modifier.addDuration('aspectOfTheShark', 'effectMultiplier', points_ * 0.4)

    pass

  def applyModification(self, collection_):

    # unlimited aspect of the sharks
    collection_.getDuration('aspectOfTheShark')._maxStacks = -1

    pass

class BeastmasterPrimalAspects(TalentBase):
  """docstring for BeastmasterPrimalAspects"""

  def __init__(self, points_):
    super(BeastmasterPrimalAspects, self).__init__(name_ = 'beastmasterPrimalAspects', points_ = points_)

    self._modifier.addDuration('aspectOfTheShark', 'duration', points_ * 0.1)
    self._modifier.addDuration('aspectOfViper', 'duration', points_ * 0.1)
    self._modifier.addDuration('aspectOfBoar', 'duration', points_ * 0.1)

    pass

class BeastmasterAncientMight(TalentBase):
  """docstring for BeastmasterAncientMight"""

  def __init__(self, points_):
    super(BeastmasterAncientMight, self).__init__(name_ = 'beastmasterAncientMight', points_ = points_)

    self._modifier.addAttribute('strength', points_)
    warnings.warn('BeastmasterAncientMight only provides strength and not flat damage yet.')

    pass

############################################################################################
############################################################################################
# Talent access class
############################################################################################
############################################################################################

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

  def applyModification(self, collection_):
    return self._talent.applyModification(collection_)