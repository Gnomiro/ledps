import skill_rework as skill

d = skill.Rive()
d.setTalent(cadence = 1, flurry = 6, nothing = 1, sever = 3, twistingFangs = 3)

for i in range(6):
  damage, attacktime, durations = d.attack()
  print(attacktime)
