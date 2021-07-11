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
    self._modifier.addIncrease('meleeAttackSpeed', 0.6)

    # assume howl as always active (frenzy, generic increase)
    self._modifier.addIncrease('meleeAttackSpeed', 0.2)
    # self._modifier.addIncrease('castSpeed', 0.2)
    self._modifier.addIncrease('generic', 0.5)

    # helmet
    self._modifier.addDuration('aspectOfTheShark', 'effect', 0.46)
    self._modifier.addDuration('aspectOfTheViper', 'effect', 0.39)

    # Body Armour
    self._modifier.addDuration('aspectOfTheShark', 'effect', 0.69)

    # Relic
    self._modifier.addDuration('aspectOfTheShark', 'effect', 0.20)
    self._modifier.addIncrease('poison', 0.6)
    self._modifier.addDuration('bleed', 'onHit', 0.37)

    # Gloves
    self._modifier.addIncrease('meleeAttackSpeed', 0.15)
    self._modifier.addAttribute('strength', 8)

    # Boots
    self._modifier.addAttribute('strength', 8)

    # rings amulet and belt unknown
    # set attributes to mactch character screen
    self._modifier.addAttribute('strength', 18)
    self._modifier.addAttribute('dexterity', 16)
    # melee attack speed provided by base-type
    self._modifier.addIncrease('meleeAttackSpeed', 0.15)

    # Weapon
    self._modifier.addMore('meleeAttackSpeed', 0.97)
    self._modifier.addIncrease('poison', 1.92)
    self._modifier.addIncrease('meleeAttackSpeed', 0.48)
    self._modifier.addAttribute('strength', 10)
    self._modifier.addAttribute('dexterity', 10)
    # other attributes do not scale serpent strike and thus are ignored
    self._modifier.addDuration('poison', 'onHit', 0.96)

    # adorned heorot idol 1 (3x)
    self._modifier.addDuration('aspectOfTheShark', 'duration', 0.23 * 3)
    # self._modifier.addDuration('aspectOfTheBoar', 'effect', 0.11) # provides defence only

    # eterran idol 1 (2x)
    self._modifier.addIncrease('overTime', 0.1 * 2)
    self._modifier.addIncrease('poison', 0.08 * 2)

    # grand heorot idol 1
    self._modifier.addDuration('poison', 'onHit', 0.2)
    self._modifier.addDuration('aspectOfTheViper', 'effect', 0.17)
    # grand heorot idol 2
    self._modifier.addDuration('poison', 'onHit', 0.2)
    self._modifier.addDuration('aspectOfTheViper', 'effect', 0.17)
    pass

  def setExamplePaladinEquipment(self):

    # blessings
    self._modifier.addDuration('physicalShred', 'onHit', 0.45)
    self._modifier.addDuration('ignite', 'onHit', 0.89)
    self._modifier.addDuration('bleed', 'onHit', 0.87)

    # sigils of hope
    empoweringSigils = 3
    numberOfSigils = 4
    self._modifier.addIncrease('generic', 0.06 * empoweringSigils * numberOfSigils)

    # holy aura
    factor = 1
    callToArms = 4
    fanaticism = 4
    self._modifier.addIncrease('generic', 0.3 * factor)
    self._modifier.addIncrease('physical', 0.1 * callToArms * factor)
    self._modifier.addIncrease('meleeAttackSpeed', 0.04 * fanaticism * factor)

    self._modifier.addIncrease('physical', 0.32)
    self._modifier.addDuration('bleed', 'duration', 0.16)
    self._modifier.addDuration('bleed', 'effect', 0.34)
    self._modifier.addIncrease('physical', 0.99)
    self._modifier.addPenetration('physical', 0.08)
    self._modifier.addMore('meleeAttackSpeed', 1.24)
    self._modifier.addIncrease('overTime', 0.43)
    self._modifier.addIncrease('meleeAttackSpeed', 0.22)
    self._modifier.addIncrease('physical', 0.68)
    self._modifier.addDuration('bleed', 'onHit', 1.05)
    self._modifier.addIncrease('physical', 0.58)
    self._modifier.addDuration('bleed', 'duration', 0.29)
    self._modifier.addDuration('bleed', 'effect', 0.67)
    self._modifier.addIncrease('physical', 0.34)
    self._modifier.addAttribute('strength', 8)
    self._modifier.addIncrease('physical', 0.56)
    self._modifier.addIncrease('physical', 0.51)
    self._modifier.addIncrease('damageOverTime', 0.19)
    self._modifier.addIncrease('meleeAttackSpeed', 0.39)
    self._modifier.addAttribute('strength', 2)
    self._modifier.addDuration('bleed', 'onHit', 0.46)
    self._modifier.addDuration('bleed', 'duration', 0.48)
    self._modifier.addDuration('bleed', 'duration', 0.2)
    self._modifier.addIncrease('physicalOverTime', 0.52)
    self._modifier.addIncrease('overTime', 0.1)
    self._modifier.addIncrease('overTime', 0.08)
    self._modifier.addIncrease('physical', 0.08)
    self._modifier.addIncrease('overTime', 0.05)
    self._modifier.addDuration('bleed', 'onHit', 0.12)
    self._modifier.addTrigger('manifestStrike', 'onMeleeHit', 0.1)
    self._modifier.addDuration('bleed', 'onHit', 0.11)
    self._modifier.addDuration('bleed', 'onHit', 0.36)
    self._modifier.addDuration('bleed', 'onHit', 0.2)
    self._modifier.addDuration('bleed', 'onHit', 0.12)
    pass