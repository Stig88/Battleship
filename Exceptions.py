class LorenIpsumException(Exception):
    pass

class BoardOutException(LorenIpsumException):
    def __init__(self, message='Выбранная точка находится вне доски!'):
        super().__init__(message)

class InvalidPlacementException(LorenIpsumException):
    def __init__(self, message='Недопустимое размещение корабля!'):
        super().__init__(message)

class DoubleTapException(LorenIpsumException):
    def __init__(self, message='Нельзя стрелять в точку повторно!'):
        super().__init__(message)

class OverlapShotException(LorenIpsumException):
    def __init__(self, message='Нельзя стрелять в зону вокруг подбитого корабля!'):
        super().__init__(message)