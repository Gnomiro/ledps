import errors

# Ailemnts with element, base damage, duration, stacksize and tags for relevant scaling attributes
durationData = {'bleed'         : { 'element' : 'physical', 'type' : 'damagingAilment', 'baseDamage' :  53. , 'condition': None, 'baseDuration' : 4., 'maxStack' : 0,
                                    'tags' : ['generic', 'physical', 'physicalOverTime', 'overTime']},
                'doom'          : { 'element' : 'void', 'type' : 'damagingAilment', 'baseDamage' :  400. , 'condition': None, 'baseDuration' : 4., 'maxStack' : 4,
                                    'tags' : ['generic', 'void', 'voidOverTime', 'overTime']}, # todo: incomplete, no inc melee damage taken buff; limit not accounted for -> oldest should be removed
                # poison scaling via poisonShred
                'poison'        : { 'element' : 'poison', 'type' : 'damagingAilment', 'baseDamage' :  20. , 'condition': None, 'baseDuration' : 3., 'maxStack' : 0,
                                    'tags' : ['generic', 'poison', 'poisonOverTime', 'overTime']}, # incomplete
                'ignite'        : { 'element' : 'fire', 'type' : 'damagingAilment', 'baseDamage' :  33. , 'condition': None, 'baseDuration' : 3., 'maxStack' : 0,
                                    'tags' : ['generic', 'fire', 'fireOverTime', 'overTime']}, # incomplete

                'physicalShred' : { 'element' : 'physical', 'type' : 'shred', 'baseDamage' :  0. , 'condition': None, 'baseDuration' : 4., 'maxStack' : 20,
                                    'tags' : []},
                'fireShred'     : { 'element' : 'fire', 'type' : 'shred', 'baseDamage' :  0. , 'condition': None, 'baseDuration' : 4., 'maxStack' : 20,
                                    'tags' : []},
                'poisonBuiltinShred'   : { 'element' : 'poison', 'type' : 'shred', 'baseDamage' : 0. , 'condition': None, 'baseDuration' : 3., 'maxStack' : 0,
                                    'tags' : []},
                'poisonShred'   : { 'element' : 'poison', 'type' : 'shred', 'baseDamage' :  0. , 'condition': None, 'baseDuration' : 4., 'maxStack' : 20,
                                    'tags' : []},

                'riveExecution' : {'element' : 'physical', 'type' : 'buff', 'increase' : .15, 'more' : .0, 'condition': None, 'baseDuration' : 2., 'maxStack' : 0,
                                    'tags' : []},
                'undisputed'    : {'element' : 'physical', 'type' : 'buff', 'increase' : .05, 'more' : .0, 'condition': 'bleed', 'baseDuration' : 4., 'maxStack' : 51,
                                    'tags' : []}
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

supportedDurationTypes = ['shred', 'damagingAilment', 'buff', 'cooldown']

supportedElementTypes = ['generic', 'physical', 'poison', 'fire', 'void']

# available attributes providing scaling
supportedTags  =  [ 'meleeAttackSpeed',
                    'generic', 'overTime',
                    'physical', 'physicalOverTime',
                    'fire', 'fireOverTime',
                    'poison', 'poisonOverTime',
                    'void', 'voidOverTime'
                  ]

supportedAttributes  = ['strength', 'dexterity']

# todo: generate this list automagically from skill.py?!
supportedSkills = ['Default', 'Melee', 'Spell', 'Throw', 'Rive', 'ManifestStrike', 'SentinelAxeThrower', 'RiveIndomitable']
# each skill procc must have a corresponding skill class
# todo: rename to trigger
# todo: remove donition again?
supportedProcs = {  'ManifestStrike'          : {'type' : 'skill', 'condition' : None},
                    'SentinelAxeThrower'      : {'type' : 'skill', 'condition' : None},
                    'RiveIndomitable'         : {'type' : 'skill', 'condition' : None},
                 }
supportedProcModifiers = ['onHit', 'onMeleeHit', 'onSpellHit', 'onThrowHit']

def getTrigger():
  return supportedProcs

# get supported ailments from ailment class
supportedDurations          = durationData.keys()
supportedDurationModifiers  = ['onHit', 'onSpellHit', 'onMeleeHit', 'onThrowHit', 'duration', 'effect']

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