from django import template


register = template.Library()


@register.inclusion_tag('posts/_post_node.html')
def post_node(post):
    return {'post': post}
