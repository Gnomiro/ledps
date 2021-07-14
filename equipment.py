import modifier

import warnings

class Equipment():
  """docstring for Equipment"""

  def __init__(self):
    self._modifier = modifier.Modifier()

  def getModifier(self):
    warnings.warn('Equipment does not look for changes currently.')
    return self._modifier

  def setExampleBeastmasterEquipment(self):

    # assume berserker as always active
    self._modifier.addIncrease(0.6, 'melee', 'speed')

    # assume howl as always active (frenzy, generic increase)
    self._modifier.addIncrease(0.2, 'melee', 'speed')
    self._modifier.addIncrease(0.2, 'spell', 'speed')
    self._modifier.addIncrease(0.5)

    # helmet
    self._modifier.addDuration('aspectOfTheShark', 0.46, 'effect')
    self._modifier.addDuration('aspectOfTheViper', 0.39, 'effect')

    # Body Armour
    self._modifier.addDuration('aspectOfTheShark', 0.69, 'effect')

    # Relic
    self._modifier.addDuration('aspectOfTheShark', 0.20, 'effect')
    self._modifier.addIncrease(0.6, 'poison')
    self._modifier.addDuration('bleed', 0.37, 'onHit')

    # Gloves
    self._modifier.addIncrease(0.15, 'melee', 'speed')
    self._modifier.addAttribute(8., 'strength')

    # Boots
    self._modifier.addAttribute(8., 'strength')

    # rings amulet and belt unknown
    # set attributes to mactch character screen
    self._modifier.addAttribute(18., 'strength')
    self._modifier.addAttribute(16., 'dexterity')
    # melee attack speed provided by base-type
    self._modifier.addIncrease(0.15, 'melee', 'speed')

    # Weapon
    self._modifier.addMore(-0.03, 'melee', 'speed')
    self._modifier.addIncrease(1.92, 'poison')
    self._modifier.addIncrease(0.48, 'melee', 'speed')
    self._modifier.addAttribute(10., 'strength')
    self._modifier.addAttribute(10., 'dexterity')
    # other attributes do not scale serpent strike and thus are ignored
    self._modifier.addDuration('poison', 0.96, 'onHit')

    # adorned heorot idol 1 (3x)
    self._modifier.addDuration('aspectOfTheShark', 0.23 * 3, 'duration')
    # self._modifier.addDuration('aspectOfTheBoar', 'effect', 0.11) # provides defence only

    # eterran idol 1 (2x)
    self._modifier.addIncrease(0.1 * 2, 'dot')
    self._modifier.addIncrease(0.08 * 2, 'poison')

    # grand heorot idol 1
    self._modifier.addDuration('poison', 0.2, 'onHit')
    self._modifier.addDuration('aspectOfTheViper', 0.17, 'effect')
    # grand heorot idol 2
    self._modifier.addDuration('poison', 0.2, 'onHit')
    self._modifier.addDuration('aspectOfTheViper', 0.17, 'effect')
    pass

  def setExamplePaladinEquipment(self):

    # blessings
    self._modifier.addDuration('physicalShred', 0.45, 'onHit')
    self._modifier.addDuration('ignite', 0.89, 'onHit')
    self._modifier.addDuration('bleed', 0.87, 'onHit')

    # sigils of hope
    empoweringSigils = 3
    numberOfSigils = 4
    self._modifier.addIncrease(0.06 * empoweringSigils * numberOfSigils)

    # holy aura
    factor = 1
    callToArms = 4
    fanaticism = 4
    self._modifier.addIncrease(0.3 * factor)
    self._modifier.addIncrease(0.1 * callToArms * factor, 'physical')
    self._modifier.addIncrease(0.04 * fanaticism * factor, 'speed', 'melee')

    self._modifier.addIncrease(0.32, 'physical')
    self._modifier.addDuration('bleed', 0.16, 'duration')
    self._modifier.addDuration('bleed', 0.34, 'effect')
    self._modifier.addIncrease(0.99, 'physical')
    self._modifier.addPenetration(0.08, 'physical')
    self._modifier.addMore(0.24, 'speed', 'melee')
    self._modifier.addIncrease(0.43, 'dot')
    self._modifier.addIncrease(0.22, 'melee' ,'speed')
    self._modifier.addIncrease(0.68, 'physical')
    self._modifier.addDuration('bleed', 1.05, 'onHit')
    self._modifier.addIncrease(0.58, 'physical')
    self._modifier.addDuration('bleed', 0.29, 'duration')
    self._modifier.addDuration('bleed', 0.67, 'effect')
    self._modifier.addIncrease(0.34, 'physical')
    self._modifier.addAttribute(8., 'strength')
    self._modifier.addIncrease(0.56, 'physical')
    self._modifier.addIncrease(0.51, 'physical')
    self._modifier.addIncrease(0.19, 'dot')
    self._modifier.addIncrease(0.39, 'melee', 'speed')
    self._modifier.addAttribute(2., 'strength')
    self._modifier.addDuration('bleed', 0.46, 'onHit')
    self._modifier.addDuration('bleed', 0.48, 'duration')
    self._modifier.addDuration('bleed', 0.2, 'duration')
    self._modifier.addIncrease(0.52, 'physical', 'dot')
    self._modifier.addIncrease(0.1, 'dot')
    self._modifier.addIncrease(0.08, 'dot')
    self._modifier.addIncrease(0.08, 'physical')
    self._modifier.addIncrease(0.05, 'dot')
    self._modifier.addDuration('bleed', 0.12, 'onHit')
    self._modifier.addTrigger('manifestStrike', 0.1, 'onHit', 'melee')
    self._modifier.addDuration('bleed', 0.11, 'onHit')
    self._modifier.addDuration('bleed', 0.36, 'onHit')
    self._modifier.addDuration('bleed', 0.2, 'onHit')
    self._modifier.addDuration('bleed', 0.12, 'onHit')
    pass