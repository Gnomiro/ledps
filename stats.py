from data import supportedTags, supportedAttributes, supportedDurations, supportedDurationModifiers, supportedElementTypes, durationData, supportedProcs, supportedProcModifiers

class Stats():

  def __init__(self, buffs_ = None):
    # todo: make getter for more/increase/... which combine relevant increases for skills/ailments
    # quest: keep scaling coefficients as list or single values? Can values be updated on the fly?
    # empty charcter sheet
    # increase modifiers
    self.increase = dict.fromkeys(supportedTags, 0.)
    # more modifiers
    self.more = dict.fromkeys(supportedTags, 1.)
    # penetration
    self.penetration = dict.fromkeys(supportedElementTypes, 0.)
    # attribute
    self.attribute = dict.fromkeys(supportedAttributes, 0.)
    # calculates ailment dict based on cross product of ailments and ailment modifers
    self.duration = {d: {dm: 0. for dm in supportedDurationModifiers} for d in supportedDurations}

    self.proc = {p: {pm: 0. for pm in supportedProcModifiers} for p in supportedProcs}

    # buffs proivide which must be accumulated into stat object
    if buffs_ != None:

      # count active buffs
      buffCount = dict()
      for buff in [b.name for b in buffs_]:
        if buff in buffCount:
          buffCount[buff] += 1
        else:
          buffCount[buff] = 1
      # print(buffCount)

      # apply specific increases and more multipliers per stack into corresponding stat-slot
      # consider maxStack if provided by buff
      # assuming that same more multipliers are still additive
      for bkey in buffCount.keys():
        # print(bkey)
        # print(buffCount[bkey])
        self.increase[durationData[bkey]['element']] += durationData[bkey]['increase'] * (buffCount[bkey] if durationData[bkey]['maxStack'] == 0 else min(buffCount[bkey], durationData[bkey]['maxStack']))
        self.more[durationData[bkey]['element']] *= (1. + durationData[bkey]['more'] * (buffCount[bkey] if durationData[bkey]['maxStack'] == 0 else min(buffCount[bkey], durationData[bkey]['maxStack'])))
      pass

    # print(self)

    pass

  def __str__(self):
    return 'increases:\n' + str(self.increase) + '\nmore:\n' + str(self.more) + '\npenetration:\n' + str(self.penetration) + '\nattribute:\n' + str(self.attribute) + '\nailments:\n' + str(self.duration)

  # class function
  def paladin(self):
    self.increase['physical'] += 1.
    self.increase['fire'] += 1.
    self.attribute['strength'] += 2
    pass

  # sentinel tree talents
  def juggernaut(self, points = 8):
    self.attribute['strength'] += points
    pass

  def blademaster(self, points = 5):
    self.increase['meleeAttackSpeed'] += 0.06 * points
    pass

  def axeThrower(self, points = 5):
    self.proc['AxeThrower']['onHit'] += points * 0.08
    pass

  # palading tree talents
  def penance(self, points = 10):
    self.duration['bleed']['onHit'] += points * 0.2
    pass

  def conviction(self, points = 8):
    self.increase['physical'] += .04 * points
    self.penetration['physical'] += .04 * points
    self.increase['fire'] += .02 * points
    self.penetration['fire'] += .02 * points
    pass

  def redemption(self, points = 7, recentlyHit = False):
    self.duration['bleed']['effect'] += 0.07 * points
    if recentlyHit:
      self.increase['generic'] += 0.07 * points
    pass

  def reverenceOfDuality(self, points = 12):
    self.increase['generic'] += 0.02 * points
    pass

  # paladin skills with talents
  # manage active part later as buff
  def holyAura(self, callToArms = 0, fanaticism = 0, active = False):
    factor = (2. if active else 1.) # effects doubled if aura active
    self.increase['generic'] += 0.3 * factor
    self.increase['physical'] += 0.1 * callToArms * factor
    self.increase['meleeAttackSpeed'] += 0.04 * fanaticism * factor
    pass

  def sigilsOfHope(self, tetragram = False, empoweringSigils = 5, numberOfSigils = None):
    # if numberOfSigils is not proved maximum number is assumed
    if numberOfSigils == None:
      if tetragram:
        numberOfSigils = 4
      else:
        numberOfSigils = 3
    self.increase['generic'] += 0.06 * empoweringSigils * numberOfSigils
    pass

  # gear add functions
  def addHelmet(self):
    self.increase['physical'] += 0.36
    self.duration['bleed']['effect'] += 0.34
    self.duration['bleed']['duration'] += 0.18
    pass

  def addAmulet(self):
    self.increase['physical'] += 0.99
    self.penetration['physical'] += 0.05
    pass

  def addSword(self):
    print("Sword")
    # implcits
    self.more['meleeAttackSpeed'] *= 1.24
    self.increase['overTime'] += 0.48
    # stats
    self.increase['meleeAttackSpeed'] += 0.22
    self.increase['physical'] += 1.03
    self.duration['bleed']['onHit'] += 0.49
    pass

  def addAxe(self):
    print("Axe")
    # implicits
    self.more['meleeAttackSpeed'] *= 1.05
    self.duration['bleed']['onHit'] += 0.3
    # stats
    self.increase['meleeAttackSpeed'] += 0.22
    self.increase['physical'] += 1.03
    self.duration['bleed']['onHit'] += 0.49
    pass

  def addUndisputed(self):
    print("Undisputed")
    # implicits
    self.more['meleeAttackSpeed'] *= 1.05
    self.duration['bleed']['onHit'] += 0.3
    # stats
    self.increase['meleeAttackSpeed'] += 0.27
    self.proc['Undisputed']['onHit'] += 1.0
    pass

  def addChest(self):
    self.increase['physical'] += 0.58
    self.duration['bleed']['effect'] += 0.67
    self.duration['bleed']['duration'] += 0.29
    pass

  def addShield(self):
      pass

  def addRing1(self):
    self.increase['physical'] += 0.53
    self.increase['overTime'] += 0.33
    pass

  def addBelt(self):
    self.increase['physical'] += 0.56
    pass

  def addRing2(self):
    self.increase['physical'] += 0.51
    self.increase['overTime'] += 0.19
    pass

  def addGloves(self):
    self.increase['meleeAttackSpeed'] += 0.39
    pass

  def addBoots(self):
    self.increase['overTime'] += 1.17
    pass

  def addRelic(self):
    self.duration['bleed']['onHit'] += 0.46
    self.duration['bleed']['duration'] += 0.48
    pass

  def addIdol(self):
    self.duration['bleed']['duration'] += 0.2
    self.increase['physicalOverTime'] += 0.52
    pass

  # generic add functions
  def addManifestStrike(self, value):
    self.proc['ManifestStrike']['onHit'] += value
    pass

  def addChanceToBleed(self, value):
    self.duration['bleed']['onHit'] += value
    pass

  def addChanceToIgnite(self, value):
    self.duration['ignite']['onHit'] += value
    pass

  def addChanceToPoison(self, value):
    self.duration['poison']['onHit'] += value
    pass

  def addChanceToPoisonShred(self, value):
    self.duration['poisonShred']['onHit'] += value
    pass

  def addStrength(self, value):
    self.attribute['strength'] += value
    pass

  def addPhysicalShred(self, value):
    self.duration['physicalShred']['onHit'] += value
    pass

  def addIncreasedOverTime(self, value):
    self.increase['overTime'] += value
    pass

  def addIncreasedPhysical(self, value):
    self.increase['physical'] += value
    pass

  def addMoreOverTime(self, value):
    self.more['overTime'] *= value
    pass

  def addMorePhysical(self, value):
    self.more['physical'] *= value
    pass

  def addMoreGeneric(self, value):
    self.more['generic'] *= value
    pass