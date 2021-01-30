from typing import Optional
from random import random, choice

from model import Beast, PARAMS
from constants import MUTATION_PERCENTAGE, MUTATION_SUCCESS, MUTATION_VALUE


def mix_same_skills(skills1: dict, skills2: dict) -> Optional[dict]:
    skill_keys = skills1.keys()
    if skill_keys != skills2.keys():
        return
    skills = {}
    for key in skill_keys:
        value = choice((skills1[key], skills2[key]))
        if random() < MUTATION_PERCENTAGE / 100:
            mutation_value = value * MUTATION_VALUE // 100
            if random() >= MUTATION_SUCCESS / 100:
                mutation_value = -mutation_value
                if value + mutation_value < 0:
                    value = 0
            elif PARAMS[key]['percent'] and value + mutation_value > 100:
                value = 100
            else:
                value += mutation_value
        gte_key = PARAMS[key].get('gte')
        if gte_key:
            min_value = skills.get(gte_key, 0)
            if value < min_value:
                value = min_value
        skills[key] = value
    return skills


def same_sex_reproduction(beast1: Beast, beast2: Beast) -> Optional[Beast]:
    if beast1.race == beast2.race and beast1 is not beast2:
        # decrease resources
        return type(beast1)(mix_same_skills(beast1.skills, beast2.skills))


def action(beast):
    pass
