from django import template

register = template.Library()

censor_dict = {'росс': 'р**с',
               'москов': 'м****в',
               'русск': 'р***к',
               'Росс': 'Р**с',
               'США': 'С*А',
               'Колорадо': 'К******о',
               'Трамп': 'Т***п'}


@register.filter(name='censor')
def censor(value):
    if isinstance(value, str):
        result = str(value)
        for key in censor_dict.keys():
            result = result.replace(key, censor_dict[key])
        return result
    else:
        raise ValueError(f'Нельзя фильтровать то, что отличается от {type(value)}')
