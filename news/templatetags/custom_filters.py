from django import template
from profanity_filter import ProfanityFilter

# если мы не зарегестрируем наши фильтры, то django никогда
# не узнает где именно их искать и фильтры потеряются(
register = template.Library()


# регестрируем наш фильтр под именем profanity, чтоб django
# понимал, что это именно фильтр, а не простая функция
# первый аргумент здесь это то значение, к которому надо
# применить фильтр
@register.filter(name='profanity')
def profanity(text):
    # возвращаемое функцией значение — это то значение, которой подставится
    # к нам в шаблон
    pf_filter = ProfanityFilter(languages=['ru', 'en'])
    return pf_filter.censor(text)
