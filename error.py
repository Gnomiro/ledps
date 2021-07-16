class MissingDurationArgument(Exception):

  def __init__(self, name_, required_, **provided_):
    self.message = 'Error: Duration object \'{}\' requires \'{}\' but received \'{}\' only.'.format(name_, required_, provided_.keys())
    super().__init__(self.message)
    pass

class InvalidElement(Exception):

  def __init__(self, element_):
    self.message = 'Error: \'{}\' is an invalid element.'.format(element_)
    super().__init__(self.message)
    pass

class InvalidDuration(Exception):

  def __init__(self, duration_):
    self.message = 'Error: \'{}\' is an invalid duration.'.format(duration_)
    super().__init__(self.message)
    pass

class InvalidDurationType(Exception):

  def __init__(self, duration_):
    self.message = 'Error: \'{}\' is an invalid duration type.'.format(duration_)
    super().__init__(self.message)
    pass

class UnsupportedSkill(Exception):

  def __init__(self, skill_):
    self.message = 'Error: \'{}\' is an unsupported skill.'.format(skill_)
    super().__init__(self.message)
    pass

class UnsupportedClass(Exception):

  def __init__(self, skill_):
    self.message = 'Error: \'{}\' is an unsupported class.'.format(skill_)
    super().__init__(self.message)
    pass

class InvalidMastery(Exception):

  def __init__(self, class_, mastery_):
    self.message = 'Error: \'{}\' is an invalid mastery for class \'{}\'.'.format(mastery_, class_)
    super().__init__(self.message)
    pass

class MissingContainerType(Exception):

  def __init__(self, name_, keys_, **types_):
    self.message = 'Error: \'{}\' requires a key from {} but only got {}.'.format(name_, keys_, types_.keys())
    super().__init__(self.message)
    pass

class InvalidContainerKey(Exception):

  def __init__(self, name_, key_, *keys_):
    self.message = 'Error: \'{}\' does not support key \'{}\' but only \'{}\'.'.format(name_, key_, keys_)
    super().__init__(self.message)
    pass