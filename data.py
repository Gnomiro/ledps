from itertools import chain

import errors

# Ailemnts with element, base damage, duration, stacksize and tags for relevant scaling attributes
durationData = {'bleed'         : { 'element' : 'physical', 'type' : 'damagingAilment', 'baseDamage' :  53. , 'condition': None, 'baseDuration' : 4., 'maxStack' : 0,
                                    'tags' : ['generic', 'physical', 'physicalOverTime', 'overTime']},
                'doom'          : { 'element' : 'void', 'type' : 'damagingAilment', 'baseDamage' :  400. , 'condition': None, 'baseDuration' : 4., 'maxStack' : 4,
                                    'tags' : ['generic', 'void', 'voidOverTime', 'overTime']},
                # poison scaling via poisonShred
                'poison'        : { 'element' : 'poison', 'type' : 'damagingAilment', 'baseDamage' :  20. , 'condition': None, 'baseDuration' : 3., 'maxStack' : 0,
                                    'tags' : ['generic', 'poison', 'poisonOverTime', 'overTime']},
                'ignite'        : { 'element' : 'fire', 'type' : 'damagingAilment', 'baseDamage' :  33. , 'condition': None, 'baseDuration' : 3., 'maxStack' : 0,
                                    'tags' : ['generic', 'fire', 'fireOverTime', 'overTime']},

                'physicalShred' : { 'element' : 'physical', 'type' : 'shred', 'baseDamage' :  0. , 'condition': None, 'baseDuration' : 4., 'maxStack' : 20,
                                    'tags' : []},
                'fireShred'     : { 'element' : 'fire', 'type' : 'shred', 'baseDamage' :  0. , 'condition': None, 'baseDuration' : 4., 'maxStack' : 20,
                                    'tags' : []},
                'poisonBuiltinShred'   : { 'element' : 'poison', 'type' : 'shred', 'baseDamage' : 0. , 'condition': None, 'baseDuration' : 3., 'maxStack' : 0,
                                    'tags' : []},
                'poisonShred'   : { 'element' : 'poison', 'type' : 'shred', 'baseDamage' :  0. , 'condition': None, 'baseDuration' : 4., 'maxStack' : 20,
                                    'tags' : []},

                # type: buff
                # general buffs applied by all hits; applied by default attack skills
                'undisputed'    : {'element' : 'physical', 'type' : 'buff', 'increase' : .05, 'more' : .0, 'condition': 'bleed', 'baseDuration' : 4., 'maxStack' : 51,
                                    'tags' : []},

                # type: skillProvidedBuff
                # buffs provided by skills; to be applied in skill implementation(mostly skillEffect)
                'riveExecution' : {'element' : 'physical', 'type' : 'skillProvidedBuff', 'increase' : .15, 'more' : .0, 'condition': None, 'baseDuration' : 2., 'maxStack' : 0,
                                    'tags' : []},
              }

# returns durationData object, if type specified only specific type
def getDurationData(*type_):

  # return all if no type specified
  if not type_:
    return durationData
  elif all([t in supportedDurationTypes for t in type_]):
    return  {k : durationData[k] for k in durationData if durationData[k]['type'] in type_}
  else:
    raise errors.InvalidDurationTypeError

supportedDurationTypes = ['shred', 'damagingAilment', 'buff', 'skillProvidedBuff', 'cooldown']

def getSupportedDurationTypes():
  return supportedDurationTypes

supportedDurationModifiers  = ['onHit', 'onSpellHit', 'onMeleeHit', 'onThrowHit', 'duration', 'effect']

def getSupportedDurationModifiers():
  return supportedDurationModifiers

supportedElementTypes = ['generic', 'physical', 'poison', 'fire', 'void']

def getSupportedElementTypes():
  return supportedElementTypes

# available attributes providing scaling
supportedTags  =  [ 'meleeAttackSpeed',
                    'generic', 'overTime',
                    'physical', 'physicalOverTime',
                    'fire', 'fireOverTime',
                    'poison', 'poisonOverTime',
                    'void', 'voidOverTime'
                  ]

def getSupportedTags():
  return supportedTags

supportedAttributes  = ['strength', 'dexterity', 'attunement']

def getSupportedAttributes():
  return supportedAttributes

supportedSkills = ['Default', 'Melee', 'Spell', 'Throw', 'Rive']

def getSupportedSkills():
  return supportedSkills

# each skill procc must have a corresponding skill class provided in skills.py
# 'onTriggerExecutions' tells how many projectiles/attacks are casted on trigger and can hit the same enemy
# possible further information: 'type', 'condition'
supportedTriggerData = {  'ManifestStrike'          : {'onHitEffectiveness' : 1., 'onTriggerExecutions' : 1},
                          'SentinelAxeThrower'      : {'onHitEffectiveness' : 1., 'onTriggerExecutions' : 1},
                          'RiveIndomitable'         : {'onHitEffectiveness' : 1., 'onTriggerExecutions' : 1},
                          'DivineBolt'              : {'onHitEffectiveness' : 1., 'onTriggerExecutions' : 1},
                       }

def getSupportedTriggerData():
  return supportedTriggerData

def getSupportedTriggers():
  return supportedTriggerData.keys()

# gear specific modifiers for Triggers
supportedTriggerModifiers = ['onHit', 'onMeleeHit', 'onSpellHit', 'onThrowHit']

def getSupportedTriggerModifiers():
  return supportedTriggerModifiers

# durations can be either applied by duration type objects or skills/triggers (cooldowns)
def getSupportedDurations():
  return chain(durationData.keys(), getSupportedSkills(), getSupportedTriggers())

# some sanity checks
# todo: how to make them only once?

# check duration elements
for d in durationData:
  if durationData[d]['element'] not in supportedElementTypes:
    raise errors.InvalidElementError

# check duration types
for d in durationData:
  if durationData[d]['type'] not in supportedDurationTypes:
    raise errors.InvalidDurationTypeError

# check duration types
for d in durationData:
    for dd in durationData[d]['tags']:
      if dd not in supportedTags:
        raise errors.InvalidTagError