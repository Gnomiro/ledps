import errors

# Ailemnts with element, base damage, duration, stacksize and tags for relevant scaling attributes
durationData = {'bleed'         : { 'element' : 'physical', 'type' : 'damagingAilment', 'baseDamage' :  53. , 'baseDuration' : 4., 'maxStack' : 0,
                                    'tags' : ['generic', 'physical', 'physicalOverTime', 'overTime']},
                # poison scaling via poisonShred
                'poison'        : { 'element' : 'poison', 'type' : 'damagingAilment', 'baseDamage' :  20. , 'baseDuration' : 3., 'maxStack' : 0,
                                    'tags' : ['generic', 'poison', 'poisonOverTime', 'overTime']}, # incomplete
                'ignite'        : { 'element' : 'fire', 'type' : 'damagingAilment', 'baseDamage' :  33. , 'baseDuration' : 3., 'maxStack' : 0,
                                    'tags' : ['generic', 'fire', 'fireOverTime', 'overTime']}, # incomple

                'physicalShred' : { 'element' : 'physical', 'type' : 'shred', 'baseDamage' :  0. , 'baseDuration' : 4., 'maxStack' : 20,
                                    'tags' : []},
                'fireShred'     : { 'element' : 'fire', 'type' : 'shred', 'baseDamage' :  0. , 'baseDuration' : 4., 'maxStack' : 20,
                                    'tags' : []},
                'poisonBuiltinShred'   : { 'element' : 'poison', 'type' : 'shred', 'baseDamage' : 0. , 'baseDuration' : 3., 'maxStack' : 0,
                                    'tags' : []},
                'poisonShred'   : { 'element' : 'poison', 'type' : 'shred', 'baseDamage' :  0. , 'baseDuration' : 4., 'maxStack' : 20,
                                    'tags' : []},

                'riveExecution' : {'element' : 'physical', 'type' : 'buff', 'increase' : .15, 'more' : .0, 'baseDuration' : 2., 'maxStack' : 0,
                                    'tags' : []},
                'undisputed'    : {'element' : 'physical', 'type' : 'buff', 'increase' : .05, 'more' : .0, 'baseDuration' : 4., 'maxStack' : 51,
                                    'tags' : []},

                'sentinelAxeThrower'  : {'element' : 'generic', 'type' : 'cooldown', 'baseDuration' : 1., 'tags' : []}, # get rid of element type and tags? -> must adapt sanity checks
              }

supportedDurationTypes = ['shred', 'damagingAilment', 'buff', 'cooldown']

supportedElementTypes = ['generic', 'physical', 'poison', 'fire']



# available attributes providing scaling
supportedTags  =  [ 'meleeAttackSpeed',
                    'generic', 'overTime',
                    'physical', 'physicalOverTime',
                    'fire', 'fireOverTime',
                    'poison', 'poisonOverTime'
                  ]

supportedAttributes  = ['strength', 'dexterity']

# each skill procc must have a corresponding skill class
supportedProcs = {  'ManifestStrike'  : {'type' : 'skill', 'condition' : None},
                    'AxeThrower'      : {'type' : 'skill', 'condition' : None}, # cooldown is simulated by 'sentinelAxeThrower' duration; no proc as long as it is active
                    'Undisputed'      : {'type' : 'buff',  'condition' : 'bleed'} # condition not used yet; hard coded in skill
                 }
supportedProcModifiers = ['onHit']

# get supported ailments from ailment class
supportedDurations          = durationData.keys()
supportedDurationModifiers  = ['onHit', 'duration', 'effect']

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