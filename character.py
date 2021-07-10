import talent, modifier, characterTalent

verbosity = 0

class CharacterInterface(object):
  """docstring for CharacterInterface"""

  def __init__(self, name_):

    self._name = name_
    self._talents = {}
    self._classModifier = modifier.Modifier()
    self._talentModifier = modifier.Modifier()
    self._prepared = True

  def getName(self):
    return self._name

  def getTalents(self):
    return self._talents

  def setTalent(self, **talents_):
    for key, value in talents_.items():
      # cast input: uncapitalize key, cast value to integer
      key, value = key[0].lower() + key[1:], int(value)
      if key in self._talents.keys():
        if value > self._talents[key][1] or value < 0:
          print('Warning: Value \'{}\' not supported for talent \'{}\' of class \'{}\'. Set to \'{}\' instead.'.format(value, key,  self._name, self._talents[key][1]))
          self._talents[key][0] = self._talents[key][1]
        else:
          self._talents[key][0] = value
      else:
        print('Warning: Talent with name \'{}\' is not available for \'{}\'. Skipped.'.format(key, self._skillName))
        continue
      if verbosity >= 1:
        print('{}: {}'.format(key, self._talents[key][0]))
      self._prepared = False
    pass

  def prepare(self):
    if not self._prepared:
      self._talentModifier = modifier.Modifier()
      for name in self._talents.keys():
        points = self._talents[name][0]
        if points != 0:
          self._talentModifier += characterTalent.Talent(name, points).getModifier()
      self._prepared = True

    def getModifier(self):
      self.prepare()
      return self._classModifier + self._talentModifier


class Sentinel(CharacterInterface):
    """docstring for Sentinel"""

  def __init__(self, name_ = 'Sentinel'):
    super(Sentinel, self).__init__(name_)

    self._classModifier.addAttribute('strength', 2)
    self._classModifier.addAttribute('vitality', 1)

    self._talents.update({'sentinelOverwhelm': [0, 5],
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


class Paladin(Sentinel):
    """docstring for Paladin"""

  def __init__(self):
    super(Paladin, self).__init__('Paladin')

    print('Warning: Paladin mastery conditional modifier always active at maximum value.')
    self._classModifier.addIncrease('physical', 1.0)
    self._classModifier.addIncrease('fire', 1.0)

    self._talents.update({'paladinConviction':[0, 8],
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
                          'paladinStaunchDefender': [0, 10],
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

class Primalist(CharacterInterface):
    """docstring for Primalist"""

  def __init__(self, name_ = 'Primalist'):
    super(Primalist, self).__init__(name_)

    print('Warning: Primalist attributes not implemented yet.')

    self._talents.update({'primalistGiftOfTheWilderness':[0, 6],
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


class Beastmaster(Primalist):
    """docstring for Beastmaster"""

  def __init__(self):
    super(Beastmaster, self).__init__('Beastmaster')

    print('Warning: Bestmaster mastery modifier not implemented yet.')

    self._talents.update({'beastmasterUrsineStrength':[0, 8],
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
                          'beastmasterHuntersOfTheDeep': [0, 4],
                          'beastmasterEnvenom': [0, 5],
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