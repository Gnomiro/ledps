import collection, duration, durationContainer, enemy, container, modifier, numpy

verbosity = 0

class Simulator:
  """docstring for Simulator"""

  def __init__(self, collection_, mainAttack_, enemy_ = None, rotationType_ = 'priority'):

    self._frametime = 0.1
    self._ticktime = 0.5

    if enemy_ == None:
      self._enemy = enemy.Enemy()
    else:
      self._enemy = enemy_
    self._mainAttack = mainAttack_
    self._rotationType = rotationType_

    self._collection = collection_

    self._durationContainer = durationContainer.DurationContainer(self._collection)

    for key, s in self._collection.getSkills().items():
      s.setDurationContainer(self._durationContainer)

  def simulate(self, endtime_ = 1000):

    self._collection.resetDurationCollection()
    self._collection.prepare()
    self._durationContainer.reset()

    t = 0
    nextattack = 0.0
    attacktime = 0

    overallDamage = container.ElementContainer()
    tickDamage = container.ElementContainer()

    buffModifier = modifier.Modifier()

    dd, sd, tickDamage = container.ElementContainer(), container.ElementContainer(), container.ElementContainer()

    while t <= endtime_:

      dd.reset()
      sd.reset()

      # allModifier = modifier.fromBuff(self._durationContainer)
      # allModifier += self._collection.getPersistentModifier()
      allModifier = modifier.ModifierChain(buffModifier.fromBuff(self._durationContainer), self._collection.getPersistentModifier())

      dd = self._durationContainer.tick(self._frametime, allModifier)

      while nextattack <= t:
        damage, attacktime = self._collection.getSkill(self._mainAttack).attack()
        sd += damage
        nextattack += attacktime

      tickDamage += dd
      tickDamage += sd

      if any(numpy.isclose([t % self._ticktime, t % self._ticktime], [0, self._ticktime], rtol = 0, atol = 0.01, equal_nan = False)):
        if verbosity >= 2:
          print('t: {}'.format(t))
          print('Overall tick damage: {}\n'.format(tickDamage))
          print(self._durationContainer.countActive())

        overallDamage += tickDamage
        tickDamage.reset()

      t += self._frametime

    # flush remaining tick damage into global
    if verbosity >= 2:
      print('t: {}'.format(t))
      print('Overall tick damage: {}\n'.format(tickDamage))
    overallDamage += tickDamage

    if verbosity >= 1:
      print('\nActive durations at end of fight:')
      print(self._durationContainer.countActive())

    if verbosity >= 1:
      print('\nActive modifiers at end of fight:')
      allModifier.merge().show()

    return overallDamage

  def someHits(self, nHits_=10):
    i = 0
    t = 0
    nextattack = 0.0
    attacktime = 0
    while not self._durationContainer.numberOfActiveDurations() != 0:
      if t == 0:
        dd = container.ElementContainer()
        sd = container.ElementContainer()
        allModifier = modifier.fromBuff(self._durationContainer)
        allModifier += self._collection.getPersistentModifier()
        if t != 0:
          dd = self._durationContainer.tick(self._frametime, allModifier)

        print('Time: {}'.format(t))
        while i < nHits_:
          if nextattack <= t:
            print('Hit: {}'.format(i))
            dmg, attacktime = self._collection.getSkill(self._mainAttack).attack()
            sd += dmg
            nextattack += attacktime
            i += 1

        print('Damage dealt in frame: {}'.format(dd + sd))
        print('Active durations: {}'.format(self._durationContainer.countActive()))
        t += self._frametime