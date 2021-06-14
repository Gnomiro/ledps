class InvalidDurationError(Exception):
  def __init__(self, message='Provided/requested duration is not supported'):
    self.message = message
    super().__init__(self.message)
    pass

class InvalidDurationTypeError(Exception):
  def __init__(self, message='Provided/requested duration type is not supported'):
    self.message = message
    super().__init__(self.message)
    pass

class InvalidDurationModifierError(Exception):
  def __init__(self, message='Provided/requested duration modifier is not supported'):
    self.message = message
    super().__init__(self.message)
    pass

class InvalidTriggerError(Exception):
  def __init__(self, message='Provided/requested trigger is not supported'):
    self.message = message
    super().__init__(self.message)
    pass

class InvalidTriggerModifierError(Exception):
  def __init__(self, message='Provided/requested trigger modifier is not supported'):
    self.message = message
    super().__init__(self.message)
    pass

class InvalidElementError(Exception):
  def __init__(self, message='Provided/requested element is not supported'):
    self.message = message
    super().__init__(self.message)
    pass

class InvalidAttributeError(Exception):
  def __init__(self, message='Provided/requested attribute is not supported'):
    self.message = message
    super().__init__(self.message)
    pass

class InvalidTagError(Exception):
  def __init__(self, message='Provided/requested tag is not supported'):
    self.message = message
    super().__init__(self.message)
    pass

class InvalidTriggerError(Exception):
  def __init__(self, message='Provided/requested trigger is not supported'):
    self.message = message
    super().__init__(self.message)
    pass