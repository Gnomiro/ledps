import stats
import skill
import simulator
import damage

import data

s = stats.Stats()

#######################################################
# Active skill buffs
#######################################################

# assume berserker as global buff
# relevant for ailments: 60% meleeAttackSpeed
s.addIncrease('meleeAttackSpeed', 0.6)

# assume howl as global buff
# relevant for ailments: 50% increased generic damage; also provides basic frenzy: 20% meleeAttackSpeed and castspeed
s.addIncrease('meleeAttackSpeed', 0.2)
s.addIncrease('castSpeed', 0.2)
s.addIncrease('generic', 0.5)

# assume frenzy totem as global buff
# scaled frenzy -> 28% meleeAttackSpeed and castspeed, 100% inc generic damage
# only one frenzy possible!

# leap slam buff (probably not permanent!)
# 100% inc generic, 30% meleeAttackSpeed and castspeed

#######################################################
# Talents
#######################################################

# base class
# 8 points in primal strength
s.addAttribute('strength', 1 * 8)

# 5 points in tempest bond with minion
s.addIncrease('physical', 0.04 * 5 * 2)

# beastmaster
# 8 points in ursine strength
s.addAttribute('strength', 1 * 8)

# 4 points in Hunters of the deep
s.addDurationModifier('aspectOfTheShark', 'duration', 0.15 * 4)

# 5 points in primal strength
s.addAttribute('strength', 1 * 5)
# boar does not provide anything for poison

# 10 points in viper fangs
s.addDurationModifier('aspectOfTheViper', 'onHit', .03 * 10)
s.addIncrease('meleeAttackSpeed', 0.05 * 10)

# 4 out of 5 points in envenom
s.addDurationModifier('poison', 'onMeleeHit', 0.03 * 4)

# 5 in circle of life and 1 point in dragon slayer
s.addDurationModifier('aspectOfTheShark', 'onHit', 0.05 * 5 * 1) # currently ignores the 5s default application and assumes boss fights!

# 8 points in ocean maw
s.addDurationModifier('aspectOfTheShark', 'effect', 0.15 * 8)
s.addDurationModifier('aspectOfTheShark', 'duration', 0.15 * 8)

# feeding frenzy hard coded: aspect of the shark modifications (for stacking) and buff effect
data.durationData['aspectOfTheShark']['maxStack'] = 0.
data.durationData['aspectOfTheShark']['effect']['increase']['meleeAttackSpeed'] = 0.04
data.durationData['aspectOfTheShark']['effect']['increase']['melee'] = 0.2

# 10 points in primal aspects
s.addDurationModifier('aspectOfTheShark', 'duration', 0.1 * 10)
s.addDurationModifier('aspectOfTheViper', 'duration', 0.1 * 10)

# 10 points in ancient might
s.addAttribute('strength', 1 * 10)

#######################################################
# Gear
#######################################################

# helmet
s.addDurationModifier('aspectOfTheShark', 'effect', 0.46)
s.addDurationModifier('aspectOfTheViper', 'effect', 0.39)

# Body Armour
s.addDurationModifier('aspectOfTheShark', 'effect', 0.69)

# Relic
s.addDurationModifier('aspectOfTheShark', 'effect', 0.20)
s.addIncrease('poison', 0.6)
s.addDurationModifier('bleed', 'onHit', 0.37)

# Gloves 
s.addIncrease('meleeAttackSpeed', 0.15)
s.addAttribute('strength', 8)

# Boots
s.addAttribute('strength', 8)

# rings amulet and belt unknown
# set attributes to mactch character screen
s.addAttribute('strength', 18)
s.addAttribute('dexterity', 16)
# melee attack speed provided by base-type
s.addIncrease('meleeAttackSpeed', 0.15)

# Weapon
s.addMore('meleeAttackSpeed', 0.97)
s.addIncrease('poison', 1.92)
s.addIncrease('meleeAttackSpeed', 0.48)
s.addAttribute('strength', 10) 
s.addAttribute('dexterity', 10) 
# other attributes do not scale serpent strike and thus are ignored
s.addDurationModifier('poison', 'onHit', 0.96)

# adorned heorot idol 1 (3x)
s.addDurationModifier('aspectOfTheShark', 'duration', 0.23 * 3)
# s.addDurationModifier('aspectOfTheBoar', 'effect', 0.11) # provides defence only

# eterran idol 1 (2x)
s.addIncrease('overTime', 0.1 * 2)
s.addIncrease('poison', 0.08 * 2)

# grand heorot idol 1
s.addDurationModifier('poison', 'onHit', 0.2)
s.addDurationModifier('aspectOfTheViper', 'effect', 0.17)
# grand heorot idol 2
s.addDurationModifier('poison', 'onHit', 0.2)
s.addDurationModifier('aspectOfTheViper', 'effect', 0.17)

#######################################################
# Serpent strike
#######################################################

skill = skill.SerpentStrike(gearStats_ = s)
skill.setTalent(scorpionStrikes = 5, chronoStrike = 5, debilitatingPoison = 1, nagasaVenom = 4, plaguebearer = 2, venomousIntent = 1) # nagasaVenom can be 6 for 20% inc poison chance

print(s)

#######################################################
# Simualtor
#######################################################

repeats = 2
endtime = 600
# boss = True reduces shred effect
boss = True
print('Boss: {}'.format(boss))
overallDamage = damage.Damage()
for i in range(repeats):
  print('\n########################## Fight {}'.format(i + 1))
  sim = simulator.Simulator(s, skill, verbosity_ = 1)
  damage = sim.combat(endtime_ = endtime, boss_ = boss)
  print("\nDamage:\n{}\nDPS:\n{}\n".format(damage, damage.dps(endtime) ))
  overallDamage += damage

print('\n########################## Result')
print("Average Damage: {}, Average DPS: {}".format(overallDamage.total() / repeats, overallDamage.total() / endtime / repeats))