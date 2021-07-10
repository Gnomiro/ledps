import modifier

class Equipment():
  """docstring for Equipment"""
  def __init__(self):
    super(Equipment, self).__init__()

    def __init__(self):
        self._modifier = modifier.Modifier()

    def getModifier(self):
        print('Warning: Equipment does not look for changes currently.')
        return self._modifier

    def setExamplePaladinEquipment(self):
        self._modifier.addDuration('physicalShred', 'onHit', 0.45)
        self._modifier.addDuration('ignite', 'onHit', 0.89)
        self._modifier.addDuration('bleed', 'onHit', 0.87)

        empoweringSigils = 3
        numberOfSigils = 4
        self._modifier.addIncrease('generic', 0.06 * empoweringSigils * numberOfSigils)

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
        self._modifier.addTrigger('ManifestStrike', 'onMeleeHit', 0.1)
        self._modifier.addDuration('bleed', 'onHit', 0.11)
        self._modifier.addDuration('bleed', 'onHit', 0.36)
        self._modifier.addDuration('bleed', 'onHit', 0.2)
        self._modifier.addDuration('bleed', 'onHit', 0.12)