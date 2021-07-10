import collection, simulator, element

collection_ = collection_.Collection()
skill_ =  collection_.getSkill('Rive')
skill_.setTalent(cadence = 1, flurry = 5, sever = 3, twistingFangs = 3, execution = 1, indomitable = 1)

character_ = collection_.getCharacter()
# character.setClass('Paladin') # todo: implement; currently paladin is constructed
character_.setTalent(paladinPenance = 10)

equipment_ = collection_.getEquipment()
equipment_.examplePaladinEquipment()

repeats = 10
endtime = 60

overallDamage = element.ElementContainer()

for i in range(repeats):
  sim = simulator.Simulator(collection_, mainAttack_ = 'Rive')

  damage = sim.simulate(endtime_ = endtime)
  print("Damage:\n{}\nDPS:\n{}\n".format(damage, damage.multiplyByFactor(1. / endtime)))
  overallDamage += damage

print("Average Damage: {}, Average DPS: {}".format(overallDamage.multiplyByFactor(1. / repeats), overallDamage.damage.multiplyByFactor(1. / endtime / repeats)))