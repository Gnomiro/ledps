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
    self._modifier.addAttribute(1. * points_, 'strength')
    pass


class SentinelBlademaster(TalentBase):
  """docstring for SentinelBlademaster"""

  def __init__(self, points_):
    super(SentinelBlademaster, self).__init__(name_ = 'SentinelBlademaster', points_ = points_)
    self._modifier.addIncrease(0.06 * points_, 'melee', 'speed')
    pass


class SentinelAxeThrower(TalentBase):
  """docstring for SentinelAxeThrower"""

  def __init__(self, points_):
    super(SentinelAxeThrower, self).__init__(name_ = 'sentinelAxeThrower', points_ = points_)
    self._modifier.addTrigger('sentinelAxeThrower', 0.08 * points_, 'onHit')
    pass

############################################################################################
# Paladin talents
############################################################################################

class PaladinPenance(TalentBase):
  """docstring for PaladinPenance"""

  def __init__(self, points_):
    super(PaladinPenance, self).__init__(name_ = 'paladinPenance', points_ = points_)
    self._modifier.addDuration('bleed', 0.08 * points_, 'onHit', 'melee')
    self._modifier.addDuration('bleed', 0.08 * points_, 'onHit', 'throwing')
    pass


class PaladinConviction(TalentBase):
  """docstring for PaladinConviction"""

  def __init__(self, points_):
    super(PaladinConviction, self).__init__(name_ = 'paladinConviction', points_ = points_)
    self._modifier.addIncrease(0.04 * points_, 'physical')
    self._modifier.addPenetration(0.02 * points_, 'physical')
    self._modifier.addIncrease(0.04 * points_, 'fire')
    self._modifier.addPenetration(0.02 * points_, 'fire')
    pass


class PaladinDivineBolt(TalentBase):
  """docstring for PaladinDivineBolt"""

  def __init__(self, points_):
    super(PaladinDivineBolt, self).__init__(name_ = 'paladinDivineBolt', points_ = points_)
    self._modifier.addTrigger('divineBolt', 0.2 * points_, 'onHit', 'melee')
    pass


class PaladinRedemption(TalentBase):
  """docstring for PaladinRedemption"""

  def __init__(self, points_):
    super(PaladinRedemption, self).__init__(name_ = 'paladinRedemption', points_ = points_)
    self._modifier.addDuration('bleed', 0.07 * points_, 'effect')
    warnings.warn('\'{}\' conditionals are disabled.'.format(self._name))
    pass


class PaladinReverenceOfDuality(TalentBase):
  """docstring for PaladinReverenceOfDuality"""

  def __init__(self, points_):
    super(PaladinReverenceOfDuality, self).__init__(name_ = 'paladinReverenceOfDuality', points_ = points_)
    self._modifier.addIncrease(0.02 * points_)
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
    self._modifier.addAttribute(1. * points_, 'strength')
    pass

class PrimalistTempestBond(TalentBase):
  """docstring for PrimalistTempestBond"""

  def __init__(self, points_):
    super(PrimalistTempestBond, self).__init__(name_ = 'primalistTempestBond', points_ = points_)
    self._modifier.addIncrease(0.04 * points_ * 2, 'physical')
    self._modifier.addIncrease(0.04 * points_ * 2, 'cold')
    self._modifier.addIncrease(0.04 * points_ * 2, 'lightning')

    warnings.warn('PrimalistTempestBond assumes minion as active.')
    pass

############################################################################################
# Beastmaster talents
############################################################################################

class BeastmasterUrsineStrength(TalentBase):
  """docstring for BeastmasterUrsineStrength"""

  def __init__(self, points_):
    super(BeastmasterUrsineStrength, self).__init__(name_ = 'beastmasterUrsineStrength', points_ = points_)
    self._modifier.addAttribute(1. * points_, 'strength')
    pass

class BeastmasterHunterOfTheDeep(TalentBase):
  """docstring for BeastmasterHunterOfTheDeep"""

  def __init__(self, points_):
    super(BeastmasterHunterOfTheDeep, self).__init__(name_ = 'beastmasterHunterOfTheDeep', points_ = points_)
    self._modifier.addDuration('aspectOfTheShark', 0.15 * points_, 'duration')
    pass

class BeastmasterPrimalStrength(TalentBase):
  """docstring for BeastmasterPrimalStrength"""

  def __init__(self, points_):
    super(BeastmasterPrimalStrength, self).__init__(name_ = 'beastmasterPrimalStrength', points_ = points_)
    self._modifier.addAttribute(1. * points_, 'strength')
    pass

class BeastmasterViperFangs(TalentBase):
  """docstring for BeastmasterViperFangs"""

  def __init__(self, points_):
    super(BeastmasterViperFangs, self).__init__(name_ = 'beastmasterViperFangs', points_ = points_)
    self._modifier.addIncrease(points_ * 0.05, 'melee', 'speed')
    self._modifier.addDuration('aspectOfTheViper', points_ * 0.03, 'onHit')
    pass

class BeastmasterEnvenom(TalentBase):
  """docstring for BeastmasterEnvenom"""

  def __init__(self, points_):
    super(BeastmasterEnvenom, self).__init__(name_ = 'beastmasterEnvenom', points_ = points_)
    self._modifier.addDuration('poison', points_ * 0.08, 'onHit', 'melee')
    pass

class BeastmasterTheCircleOfLife(TalentBase):
  """docstring for BeastmasterTheCircleOfLife"""

  def __init__(self, points_):
    super(BeastmasterTheCircleOfLife, self).__init__(name_ = 'beastmasterTheCircleOfLife', points_ = points_)
    self._modifier.addDuration('aspectOfTheShark', points_ * 0.05, 'onHit')

    warnings.warn('BeastmasterTheCircleOfLife always assumes DragonSlayer active and fight against bosses')
    pass

class BeastmasterOceanMaw(TalentBase):
  """docstring for BeastmasterOceanMaw"""

  def __init__(self, points_):
    super(BeastmasterOceanMaw, self).__init__(name_ = 'beastmasterOceanMaw', points_ = points_)
    self._modifier.addDuration('aspectOfTheShark', points_ * 0.15, 'effect')
    self._modifier.addDuration('aspectOfTheShark', points_ * 0.15, 'duration')
    pass

class BeastmasterFeedingFrenzy(TalentBase):
  """docstring for BeastmasterFeedingFrenzy"""

  def __init__(self, points_):
    super(BeastmasterFeedingFrenzy, self).__init__(name_ = 'beastmasterFeedingFrenzy', points_ = points_)

    self._modifier.addDuration('aspectOfTheShark', -points_ * 0.6, 'effect', 'more')
    warnings.warn('Check if BeastmasterFeedingFrenzy more aspectOfTheShark works this way')

    pass

  def applyModification(self, collection_):

    # unlimited aspect of the sharks
    collection_.getDuration('aspectOfTheShark')._maxStacks = -1

    pass

class BeastmasterPrimalAspects(TalentBase):
  """docstring for BeastmasterPrimalAspects"""

  def __init__(self, points_):
    super(BeastmasterPrimalAspects, self).__init__(name_ = 'beastmasterPrimalAspects', points_ = points_)

    self._modifier.addDuration('aspectOfTheShark', points_ * 0.1, 'duration')
    self._modifier.addDuration('aspectOfViper', points_ * 0.1, 'duration')
    self._modifier.addDuration('aspectOfBoar', points_ * 0.1, 'duration')

    pass

class BeastmasterAncientMight(TalentBase):
  """docstring for BeastmasterAncientMight"""

  def __init__(self, points_):
    super(BeastmasterAncientMight, self).__init__(name_ = 'beastmasterAncientMight', points_ = points_)

    self._modifier.addAttribute(1. * points_, 'strength')
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