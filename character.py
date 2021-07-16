import characterTalent, modifier, error

import warnings

verbosity = 0


##########################################################################
##########################################################################
# Basic class interface
##########################################################################
##########################################################################

class ClassInterface():
  """docstring for ClassInterface"""

  def __init__(self, name_):

    self._name = name_
    # list of available talents with point limit
    self._talents = {}
    # list of associated talent objects of active talents
    self._activeTalents = {}
    self._modifier = modifier.Modifier()
    self._talentModifier = modifier.Modifier()
    self._prepared = True

    self._mastery = None

    # self._masteries is set in class implementations
    for mastery in (self._masteries if self._masteries else []):
      m = mastery[0].upper() + mastery[1:]
      eval(m)().getLowerTalents(self._talents)
    pass

  def getClass(self):
    return self._name

  def getMastery(self):
    return self._mastery

  def setMastery(self, mastery_):
    if self._mastery == None:
      mL = mastery_[0].lower() + mastery_[1:]
      mU = mastery_[0].upper() + mastery_[1:]
      if mL in self._masteries:
        self._mastery = mL
        eval(mU)().getMasteryTalents(self._talents)
        eval(mU)().getMasteryModifer(self._modifier)
      else:
        raise error.InvalidMastery(self._name, mU)
    else:
      warnings.warn('Mastery change not supported yet.') 
    pass

  def getTalents(self):
    return self._talents

  def getClassTalents(self):
    return self._classTalents

  def setTalent(self, **talents_):
    for name, value in talents_.items():
      # cast input: uncapitalize key, cast value to integer
      talentName, points = name[0].lower() + name[1:], int(value)
      if talentName in self._talents.keys():
        if points > self._talents[talentName][1] or points < 0:
          print('Warning: Value \'{}\' not supported for talent \'{}\' of class \'{}\'. Set to \'{}\' instead.'.format(points, talentName,  self._name, self._talents[talentName][1]))
          self._talents[talentName][0] = self._talents[talentName][1]
        else:
          self._talents[talentName][0] = value
      else:
        print('Warning: Talent with name \'{}\' is not available for \'{}\'. Skipped.'.format(talentName, self._name))
        continue
      # store talent object
      self._activeTalents.update({talentName: characterTalent.Talent(talentName, self._talents[talentName][0])})
      if verbosity >= 1:
        print('{}: {}'.format(talentName, self._talents[talentName][0]))
      self._prepared = False
    pass

  def prepare(self):
    if not self._prepared:
      self._talentModifier = modifier.Modifier()
      for name in self._talents.keys():
        points = self._talents[name][0]
        if points != 0:
          self._talentModifier += self._activeTalents[name].getModifier()
      self._prepared = True

  def getModifier(self):
    self.prepare()
    return self._modifier + self._talentModifier

  def applyModification(self, collection_):
    self.prepare()
    for name, talent in self._activeTalents.items():
      for name in self._talents.keys():
        if self._talents[name][0] != 0:
          talent.applyModification(collection_)

    pass

##########################################################################
##########################################################################
# Class implementations
##########################################################################
##########################################################################

##########################################################################
# Sentinel class
##########################################################################

class Sentinel(ClassInterface):
  """docstring for Sentinel"""

  def __init__(self, name_ = 'Sentinel'):
    # self._masteries = ['voidKnight', 'paladin', 'forgeGuard']
    self._masteries = ['paladin']
    super(Sentinel, self).__init__(name_)

    self._classModifier = modifier.Modifier()

    self._classModifier.addAttribute(2., 'strength')
    self._classModifier.addAttribute(1., 'vitality')

    self._classTalents =({'sentinelOverwhelm': [0, 5],
                          'sentinelJuggernaut': [0, 8],
                          'sentinelFearless': [0, 8],
                          'sentinelCounterAttack': [0, 5],
                          'sentinelRelentless': [0, 10],
                          'sentinelArmourClad': [0, 5],
                          'sentinelGladiator': [0, 5],
                          'sentinelIronMastery': [0, 8],
                          'sentinelBanish': [0, 4],
                          'sentinelTimeAndFaith': [0, 5],
                          'sentinelAegisOfRenewal': [0, 5],
                          'sentinelGladiator': [0, 1],
                          'sentinelAxeThrower': [0, 5],
                          'sentinelBlademaster': [0, 5],
                          'sentinelMailCrusher': [0, 10],
                          })
    self._talents.update(self._classTalents)
    self._modifier += self._classModifier
    pass

##########################################################################
# Primalist class
##########################################################################

class Primalist(ClassInterface):
  """docstring for Primalist"""

  def __init__(self, name_ = 'Primalist'):
    self._masteries = ['beastmaster']
    super(Primalist, self).__init__(name_)

    print('Warning: Primalist base attributes not implemented yet.')
    self._classModifier = modifier.Modifier()

    self._classTalents = ({'primalistGiftOfTheWilderness':[0, 6],
                          'primalistNaturalAttunement': [0, 8],
                          'primalistPrimalStrength': [0, 8],
                          'primalistPrimalMedicine': [0, 6],
                          'primalistHarmonyOfBlades': [0, 1],
                          'primalistHuntersRestoration': [0, 5],
                          'primalistWisdomOfTheWild': [0, 6],
                          'primalistSurvivalOfThePack': [0, 6],
                          'primalistAncientCall': [0, 6],
                          'primalistTempestBond': [0, 8],
                          'primalistHuntersEmanation': [0, 5],
                          'primalistEldersBranch': [0, 5],
                          'primalistBerserker': [0, 5],
                          'primalistRotbane': [0, 5],
                          'primalistAncestralWeaponry': [0, 10],
                          })
    self._talents.update(self._classTalents)
    self._modifier += self._classModifier
    pass


##########################################################################
##########################################################################
# Mastery interface class
##########################################################################
##########################################################################

class MasteryInterface():
  """docstring for MasteryInterface"""

  def __init__(self):
    self._lowerTalents = {}
    self._upperTalents = {}
    self._masteryModifier = modifier.Modifier()
    pass

  def getLowerTalents(self, talents_):
    talents_.update(self._lowerTalents)
    pass

  def getMasteryModifer(self, classModifier_):
    classModifier_ += self._masteryModifier
    pass

  def getMasteryTalents(self, talents_):
    talents_.update(self._upperTalents)
    pass

##########################################################################
##########################################################################
# Mastery implementations
##########################################################################
##########################################################################

##########################################################################
# Paladin mastery
##########################################################################

class Paladin(MasteryInterface):
  """docstring for Paladin"""

  def __init__(self):
    super(Paladin, self).__init__()

    self._lowerTalents =  ({'paladinConviction':[0, 8],
                            'paladinDefiance': [0, 8],
                            'paladinHonour': [0, 5],
                            'paladinMajasaFirebrand': [0, 10],
                            'paladinDivineBolt': [0, 1],
                            'paladinValor': [0, 8],
                            'paladinHolySymbol': [0, 6],
                            'paladinFlashOfBrilliance': [0, 10],
                            'paladinRahyehsStrength': [0, 8],
                            'paladinSharedDivinity': [0, 5],
                            'paladinHolySymbol2': [0, 6],
                            'paladinHolyNove': [0, 1],
                            'paladinPrayer': [0, 10],
                            'paladinPiety': [0, 1],
                            'paladinInnerFlame': [0, 8],
                            })

    warnings.warn('Paladin mastery conditional modifier always active at maximum value.')
    self._masteryModifier.addIncrease(1., 'physical')
    self._masteryModifier.addIncrease(1., 'fire')

    # upper half
    self._upperTalents =  ({'paladinStaunchDefender': [0, 10],
                            'paladinFaithArmour': [0, 8],
                            'paladinAlignment': [0, 8],
                            'paladinShieldWall': [0, 1],
                            'paladinHolyPrecision': [0, 10],
                            'paladinPenance': [0, 10],
                            'paladinRighteousFirebrand': [0, 7],
                            'paladinPrayerAegis': [0, 10],
                            'paladinDivineEssence': [0, 5],
                            'paladinReverenceOfDuality': [0, 12],
                            'paladinRedemption': [0, 7],
                            'paladinSwordOfRahyeh': [0, 7],
                            'paladinLightOfRahyeh': [0, 12],
                            'paladinDivineIntervention': [0, 1],
                            })
    pass

##########################################################################
# Beastmaser mastery
##########################################################################

class Beastmaster(MasteryInterface):
  """docstring for Beastmaster"""

  def __init__(self):
    super(Beastmaster, self).__init__()

    print('Bestmaster mastery only implements meleed damage increase.')
    self._masteryModifier.addIncrease(.5, 'melee')


    self._lowerTalents =  ({'beastmasterUrsineStrength':[0, 8],
                            'beastmasterFelineBond': [0, 8],
                            'beastmasterSavagery': [0, 8],
                            'beastmasterBoarHeart': [0, 5],
                            'beastmasterArtorsLoyality': [0, 1],
                            'beastmasterAmbush': [0, 8],
                            'beastmasterTuskWarrior': [0, 8],
                            'beastmasterCallOfThePack': [0, 5],
                            'beastmasterLampreyTeeth': [0, 6],
                            'beastmasterPorcineConstitution': [0, 5],
                            'beastmasterTheChase': [0, 8],
                            'beastmasterRendingMaw': [0, 5],
                            'beastmasterDeepWounds': [0, 8],
                            'beastmasterPrimalStrength': [0, 5],
                            'beastmasterAxeAndClaw': [0, 5],
                            'beastmasterHunterOfTheDeep': [0, 4],
                           })

    self._upperTalents =  ({'beastmasterEnvenom': [0, 5],
                            'beastmasterHawkWings': [0, 10],
                            'beastmasterLifeInTheWilderness': [0, 8],
                            'beastmasterTheCircleOfLife': [0, 5],
                            'beastmasterViperFangs': [0, 10],
                            'beastmasterAvianShelter': [0, 10],
                            'beastmasterCryOfTheLynx': [0, 8],
                            'beastmasterDragonSlayer': [0, 1],
                            'beastmasterForceOfNature': [0, 1],
                            'beastmasterNaturalBond': [0, 1],
                            'beastmasterOceanMaw': [0, 8],
                            'beastmasterRattlesnakeRattlesnake': [0, 10],
                            'beastmasterSerratedClaws': [0, 6],
                            'beastmasterAncientMight': [0, 10],
                            'beastmasterCriticalBight': [0, 5],
                            'beastmasterPrimalAspects': [0, 10],
                            'beastmasterFeedingFrenzy': [0, 1],
                            })
    pass

  ############################################################################################
############################################################################################
# Skill implementation information
############################################################################################
############################################################################################

import sys, inspect

# base classes
baseClasses = ['classInterface', 'masteryInterface']

# collect all durations and to de-capitalize them
allClasses = [name[0].lower() + name[1:] for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass) if obj.__module__ is __name__]
characterClasses = [name[0].lower() + name[1:] for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass) if obj.__module__ is __name__ if str(inspect.getmro(obj)[1]).find('ClassInterface') != -1]
masteryClasses = [name[0].lower() + name[1:] for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass) if obj.__module__ is __name__ if str(inspect.getmro(obj)[1]).find('MasteryInterface') != -1]

# implemented class; allClasses.remove(baseClasses)
implementedClasses = [name for name in allClasses if name not in baseClasses]

def getBaseClasses():
  return baseClasses

def getAllClasses():
  return allClasses

def getImplementedClasses():
  return implementedClasses

def getCharacterClasses():
  return characterClasses

def getMasteryClasses():
  return masteryClasses