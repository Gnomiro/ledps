import stats
import skill
import character
import sys
# sys.path.append("playground/")


s = stats.Stats()

# add 100 increased physical and fire (based on HP percentage) as well as 2 strength
s.paladin()

# sentinel passives
s.juggernaut(points = 8)
s.blademaster(points = 5)
s.axeThrower(points = 1)

# paladin passives
s.conviction(points = 8)
s.penance(points = 10)
s.redemption(points = 7, recentlyHit = False)
s.reverenceOfDuality(points = 10)

# aura like skills
s.holyAura(callToArms = 4, fanaticism = 4, active = False)
s.sigilsOfHope(tetragram = True, empoweringSigils = 3)

# physical shred from blessing
s.addPhysicalShred(.45)

s.addHelmet()
s.addAmulet()
s.addSword()
# s.addAxe()
# s.addUndisputed()
s.addChest()
# does not provide any significant stats
s.addShield()
s.addRing1()
s.addBelt()
s.addRing2()
s.addGloves()
# Doom not applied; would increase stack 4 times, duration 4, and increase melee damage by 4% each
s.addBoots()
s.addRelic()

# todo:
# melee skills with modifiers 
# -> buffs especially for something like rive execution; scale linear with number of target instead of 
# simulating multiple targets
# buffs <-> ailments like 'shred' with different type like 'buff' and 'element' for increases, maybe 'generic'
# should be treated like an 'element' for this purpose
# maybe: rename 'ailment' to 'duration' with types 'damagingAilment', 'ailment', 'buff', 'shred'. 'debuff'
# maybe: store ailments <-> duration in seperate containers based on type

# if dots really snapshot damage calculation besides shred must be moved to each
# single ailment on creation instead of tick! -> shoudl even be more efficient!
# shred and other debuffs still on per tick base as it depends on debuffs on enemy?

# divine bolt on hit; same target? doesnt seem so
# manifest strike on hit
# axe thrower; same target? - seems so

# large idol
s.addIdol()
# small idol 1
s.addIncreasedOverTime(0.1)
# # small idol 2
s.addIncreasedOverTime(0.08)
s.addIncreasedPhysical(0.08)
# # small idol 3
s.addIncreasedOverTime(0.08)
s.addIncreasedPhysical(0.05)

# humble idol 1
s.addChanceToBleed(0.12)
s.addIncreasedPhysical(0.14)
# ornate idol 1
s.addManifestStrike(0.1)
# humble idol 2
s.addChanceToBleed(0.11)
# ornate idol 1
s.addChanceToBleed(0.36)
s.addChanceToBleed(0.20)
# humble idol 3
s.addChanceToBleed(0.13)
s.addIncreasedPhysical(0.14)

# print(s)

skill = skill.Rive()
skill.setTalent(cadence = 1, flurry = 5, sever = 3, twistingFangs = 3, execution = 1, indomitable = 1)

# warpath's drainingAssault adds global more damage while spinning
# drainingAssault = 5
# s.addMoreGeneric(1 + 0.15 * drainingAssault)
# skill = skill.Warpath()

repeats = 10
endtime = 60
boss = True
overallDamage = 0
for i in range(repeats):
  c = character.Character(s, skill, verbosity = 0.)
  # boss = True reduces shred effect
  damage = c.combat(endtime = endtime, boss = boss)
  print("Damage: {}, DPS: {}".format(damage, damage / endtime))
  overallDamage += damage

print("Average Damage: {}, Average DPS: {}".format(overallDamage / repeats, overallDamage / endtime / repeats))

# damage = c.singleHit()
# print("Damage: {}, DPS: {}".format(damage, damage / t))