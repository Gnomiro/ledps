import duration_rework as duration

import sys
sys.path.append("..")
import skill
import damage

d = duration.Durations()

d.add('physicalShred')
d.tick()
for i in range(22):
  print(i)
  d.add('physicalShred')
d.add('bleed')
d.add('poison')
d.add('SentinelAxeThrower', duration_ = 1, type_ = 'cooldown')

t = 0
d.removeInactive()
print([(t.getName(), t.isActive()) for t in d.getByType('cooldown', 'damagingAilment')])
print(d.countActive())

print([t.getName() for t in d.getByName('bleed', 'SentinelAxeThrower')])
print(d.countActiveByName('bleed', 'SentinelAxeThrower'))
print(d.countActiveByType('damagingAilment'))

d.tick()

d1 = damage.Damage(('physical', 5.), ('fire', 3.))
print(d1.total())
