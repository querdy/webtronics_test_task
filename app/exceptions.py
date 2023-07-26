

class BaseWebtronicsError(Exception):
    pass


class BadUserError(BaseWebtronicsError):
    pass


class DoubleReactionError(BaseWebtronicsError):
    pass


class VerifyEmailError(BaseWebtronicsError):
    pass


class UsernameAlreadyExistsError(BaseWebtronicsError):
    pass


class BadIdError(BaseWebtronicsError):
    pass


class BadUserOrIdError(BadUserError, BadIdError):
    pass
