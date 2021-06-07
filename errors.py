class InvalidDurationError(Exception):
  def __init__(self, message='Provided duration is not supported'):
    self.message = message
    super().__init__(self.message)
    pass

class InvalidDurationTypeError(Exception):
  def __init__(self, message='Provided duration type is not supported'):
    self.message = message
    super().__init__(self.message)
    pass

class InvalidElementError(Exception):
  def __init__(self, message='Provided element is not supported'):
    self.message = message
    super().__init__(self.message)
    pass

class InvalidTagError(Exception):
  def __init__(self, message='Provided tag is not supported'):
    self.message = message
    super().__init__(self.message)
    pass    