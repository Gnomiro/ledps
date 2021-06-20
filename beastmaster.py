import stats
import skill
import simulator
import damage

# assume berserker as global buff
# relevant for ailments: 60% meleeAttackSpeed

# assume howl as global buff
# relevant for ailments: 50% increased generic damage; also provides basic frenzy: 20% meleeAttackSpeed and castspeed

# assume frenzy totem as global buff
# scaled frenzy -> 28% meleeAttackSpeed and castspeed, 100% inc generic damage

# leap slam buff (probably not permanent!)
# 100% inc generic, 30% meleeAttackSpeed and castspeed

s = stats.Stats()

skill = skill.Melee()
# skill.setTalent(cadence = 1, flurry = 5, sever = 3, twistingFangs = 3, execution = 1, indomitable = 1)

s.addDurationModifier('aspectOfTheViper', 'onHit', 1.)
s.addDurationModifier('aspectOfTheShark', 'onHit', 1.)
# todo: move buff calculation out of durations into cahracter; otherwise without a damagingAilment
# buffs are never considered
s.addDurationModifier('bleed', 'onHit', 1.)

print(s)

repeats = 10
endtime = 60
# boss = True reduces shred effect
boss = False
print('Boss: {}'.format(boss))
overallDamage = damage.Damage()
for i in range(repeats):
  sim = simulator.Simulator(s, skill, verbosity_ = 0)
  damage = sim.combat(endtime_ = endtime, boss_ = boss)
  print("Damage:\n{}\nDPS:\n{}\n".format(damage, damage.dps(endtime) ))
  overallDamage += damage

print("Average Damage: {}, Average DPS: {}".format(overallDamage.total() / repeats, overallDamage.total() / endtime / repeats))