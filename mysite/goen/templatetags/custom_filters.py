from django import template

register = template.Library()


@register.filter
def get_points(ranking_list, user):
    return ranking_list[user.username + '_points']


@register.filter
def get_amount_learning_words(ranking_list, user):
    return ranking_list[user.username + '_amount_learning_words']


@register.filter
def get_amount_learned_words(ranking_list, user):
    return ranking_list[user.username + '_amount_learned_words']
