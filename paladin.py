import collection, simulator, element

collection_ = collection.Collection()
skill_ =  collection_.getSkill('rive')
skill_.setTalent(cadence = 1, flurry = 5, sever = 3, twistingFangs = 3, execution = 1,
                 indomitable = 1, ironReach = 1, tripleThreat = 1)

character_ = collection_.setCharacter('paladin')
character_.setTalent(sentinelJuggernaut = 8, sentinelAxeThrower = 1, sentinelBlademaster = 5,
                     paladinConviction = 8, paladinDivineBolt = 1, paladinPenance = 10,
                     paladinReverenceOfDuality = 8, paladinRedemption = 7)

equipment_ = collection_.getEquipment()
equipment_.setExamplePaladinEquipment()

repeats = 10
endtime = 60

overallDamage = element.ElementContainer()

sim = simulator.Simulator(collection_, mainAttack_ = 'rive')

for i in range(repeats):
  damage = sim.simulate(endtime_ = endtime)
  print("\nDamage:\n{}\nDPS:\n{}\n".format(damage, damage.multiplyByFactor(1. / endtime)))
  overallDamage += damage

print("Average Damage:\n{}\nAverage DPS:\n{}".format(overallDamage.multiplyByFactor(1. / repeats), overallDamage.multiplyByFactor(1. / endtime / repeats)))