from app import models
from app.models import ReactionType


def publication_reactions_to_dict(reactions: list[models.Reaction]) -> dict:
    _reactions = {react.value: 0 for react in ReactionType}
    for reaction in reactions:
        _reactions[reaction.type.value] += 1
    return _reactions

