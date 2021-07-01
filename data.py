from itertools import chain

import errors

# Ailemnts with element, base damage, duration, stacksize and tags for relevant scaling attributes
durationData = {'bleed'         : { 'element' : 'physical', 'type' : 'damagingAilment', 'baseDamage' :  53. , 'condition': {}, 'baseDuration' : 4., 'maxStack' : 0,
                                    'tags' : ['generic', 'physical', 'physicalOverTime', 'overTime']},
                'doom'          : { 'element' : 'void', 'type' : 'damagingAilment', 'baseDamage' :  400. , 'condition': {}, 'baseDuration' : 4., 'maxStack' : 4,
                                    'tags' : ['generic', 'void', 'voidOverTime', 'overTime']},
                # poison scaling via poisonShred
                'poison'        : { 'element' : 'poison', 'type' : 'damagingAilment', 'baseDamage' :  20. , 'condition': {}, 'baseDuration' : 3., 'maxStack' : 0,
                                    'tags' : ['generic', 'poison', 'poisonOverTime', 'overTime']},
                'ignite'        : { 'element' : 'fire', 'type' : 'damagingAilment', 'baseDamage' :  33. , 'condition': {}, 'baseDuration' : 3., 'maxStack' : 0,
                                    'tags' : ['generic', 'fire', 'fireOverTime', 'overTime']},

                # other damaging ailments
                'plague': { 'element' : 'poison', 'type' : 'damagingAilment', 'baseDamage' :  90. , 'condition': {}, 'baseDuration' : 4., 'maxStack' : 1,
                                    'tags' : ['generic', 'poison', 'poisonOverTime', 'overTime']},
                'blindingPoison': { 'element' : 'poison', 'type' : 'damagingAilment', 'baseDamage' :  30. , 'condition': {}, 'baseDuration' : 4., 'maxStack' : 1,
                                    'tags' : ['generic', 'poison', 'poisonOverTime', 'overTime']},

                'physicalShred' : { 'element' : 'physical', 'type' : 'shred', 'baseDamage' :  0. , 'condition': {}, 'baseDuration' : 4., 'maxStack' : 20,
                                    'tags' : []},
                'fireShred'     : { 'element' : 'fire', 'type' : 'shred', 'baseDamage' :  0. , 'condition': {}, 'baseDuration' : 4., 'maxStack' : 20,
                                    'tags' : []},
                'poisonBuiltinShred'   : { 'element' : 'poison', 'type' : 'shred', 'baseDamage' : 0. , 'condition': {}, 'baseDuration' : 3., 'maxStack' : 0,
                                    'tags' : []},
                'poisonShred'   : { 'element' : 'poison', 'type' : 'shred', 'baseDamage' :  0. , 'condition': {}, 'baseDuration' : 4., 'maxStack' : 20,
                                    'tags' : []},

  # type: buff
  # general buffs applied by all hits; applied by default attack skills
  # Undisputed Axe buff
  'undisputed'        : {'type' : 'buff',
                         'effect' : {'increase' : {'physical' : 0.05}},
                         'condition': {'isActive' : 'bleed'},
                         'baseDuration' : 4., 'maxStack' : 51},


  # Primalist Aspect of the Shark buff
  # default limited to one stack
  # todo: add armour shred chance
  'aspectOfTheShark' : {'type' : 'buff',
                        'effect' : {'increase' : {'meleeAttackSpeed' : 0.04, 'melee': 0.20}}, # todo: check value
                        'condition': {},
                        'baseDuration' : 3., 'maxStack' : 0},

  # Primalist Aspect of the Boar buff
  # on recentlyHit or 4% onHit per Talent (up to 20%)
  # todo: scale with talents, currently maximum stats for bleed/physical but not defence
  'aspectOfTheBoar'  : {'type' : 'buff',
                        'effect' : {'increase' : {'physical' : 0.4},
                                    'duration'  : {'bleed' : {'onHit' : 0.4, 'effect' : 1.2} }
                                   },
                        'condition': {},
                        'baseDuration' : 1., 'maxStack' : 1},

  # Primalist Aspect of the Viper buff
  # 3% onHit per Talent (up to 30%)
  # todo: talents for poison effectiveness/duration
  'aspectOfTheViper' : {'type' : 'buff',
                        'effect' : {'increase' : {'overTime' : 1.},
                                    'duration'  : {'poison' : {'onHit' : 1.} }
                                   },
                        'condition': {},
                        'baseDuration' : 3., 'maxStack' : 1},

  # type: skillProvidedBuff
  # buffs provided by skills; to be applied in skill implementation(mostly skillEffect)
  'riveExecution'     : {'type' : 'skillProvidedBuff',
                         'effect' : {'increase' : {'physical' : 0.15}},
                         'condition': {},
                         'baseDuration' : 2., 'maxStack' : 0},

  # Primalist Swipe Aspect of the Panther buff
  'swipeAspectofThePantherGeneric' : {'type' : 'skillProvidedBuff',
                                      'effect' : {'increase' : {'generic' : .1},
                                                 },
                                      'condition': {},
                                      'baseDuration' : 4., 'maxStack' : 1},
  'swipeAspectofThePantherSpeed'   : {'type' : 'skillProvidedBuff',
                                      'effect' : {'increase' : {'meleeAttackSpeed' : .15, 'castSpeed' : .15},
                                                 },
                                      'condition': {},
                                      'baseDuration' : 4., 'maxStack' : 1},

  # Primalist Serpent Strike buffs; default set to 0; modifyied in Skill implementation
  'serpentStrikeOnHit'             : {'type' : 'skillProvidedBuff',
                                      'effect' : {'increase' : {'poison' : 0., 'overTime' : 0.},
                                                 },
                                      'condition': {},
                                      'baseDuration' : 4., 'maxStack' : 0},

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
supportedTags  =  [ 'meleeAttackSpeed', 'castSpeed',
                    'generic', 'melee', 'overTime',
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

supportedSkills = ['Default', 'Melee', 'Spell', 'Throw', 'Rive', 'Swipe', 'SerpentStrike']

def getSupportedSkills():
  return supportedSkills

# each skill procc must have a corresponding skill class provided in skills.py
# 'onTriggerExecutions' tells how many projectiles/attacks are casted on trigger and can hit the same enemy
# possible further information: 'type', 'condition'
supportedTriggerData = {  'ManifestStrike'          : {'onHitEffectiveness' : 1., 'onTriggerExecutions' : 1},
                          'SentinelAxeThrower'      : {'onHitEffectiveness' : 1., 'onTriggerExecutions' : 1},
                          'RiveIndomitable'         : {'onHitEffectiveness' : 1., 'onTriggerExecutions' : 1},
                          'DivineBolt'              : {'onHitEffectiveness' : 1., 'onTriggerExecutions' : 1},
                          'SerpentStrikePoisonSpit' : {'onHitEffectiveness' : 1., 'onTriggerExecutions' : 1},
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
# for d in durationData:
#   if durationData[d]['element'] not in supportedElementTypes:
#     raise errors.InvalidElementError

# check duration types
for d in durationData:
  if durationData[d]['type'] not in supportedDurationTypes:
    raise errors.InvalidDurationTypeError

# check duration types
# for d in durationData:
#     for dd in durationData[d]['tags']:
#       if dd not in supportedTags:
#         raise errors.InvalidTagError