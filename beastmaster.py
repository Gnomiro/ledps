import collection, simulator, element

collection_ = collection.Collection()
skill_ =  collection_.getSkill('serpentStrike')
skill_.setTalent(scorpionStrikes = 5, chronoStrike = 5, debilitatingPoison = 1, nagasaVenom = 4, plaguebearer = 2, venomousIntent = 1)

character_ = collection_.setCharacter('beastmaster')
character_.setTalent(primalistPrimalStrength = 8, primalistTempestBond = 5, beastmasterUrsineStrength = 8, beastmasterHunterOfTheDeep = 4,
                     beastmasterPrimalStrength = 5, beastmasterViperFangs = 10, beastmasterEnvenom = 5, beastmasterTheCircleOfLife = 5,
                     beastmasterOceanMaw = 8, beastmasterFeedingFrenzy = 1, beastmasterAncientMight = 10, beastmasterPrimalAspects = 10)

equipment_ = collection_.getEquipment()
equipment_.setExampleBeastmasterEquipment()

repeats = 1
endtime = 600

overallDamage = element.ElementContainer()

sim = simulator.Simulator(collection_, mainAttack_ = 'serpentStrike')

for i in range(repeats):
  damage = sim.simulate(endtime_ = endtime)
  print("\nDamage:\n{}\nDPS:\n{}\n".format(damage, damage.multiplyByFactor(1. / endtime)))
  overallDamage += damage

print("Average Damage:\n{}\nAverage DPS:\n{}".format(overallDamage.multiplyByFactor(1. / repeats), overallDamage.multiplyByFactor(1. / endtime / repeats)))