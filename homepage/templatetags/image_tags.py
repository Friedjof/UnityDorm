from django import template

from homepage.images import optimized_image as build_optimized_image


register = template.Library()


@register.simple_tag
def optimized_image(image_field, width, height=None):
    return build_optimized_image(image_field, width, height)
