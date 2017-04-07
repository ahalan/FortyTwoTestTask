from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def edit_link(instance):
    """ Renders link to admin edit page of the instance """

    try:
        content_type = ContentType.objects.get_for_model(instance.__class__)
    except AttributeError:
        raise ValueError('Passed value must be registered model instance')
    else:
        model_admin_change_link = 'admin:{app}_{model}_change'.format(
            app=content_type.app_label,
            model=content_type.model
        )
        return reverse(model_admin_change_link, args=(instance.id,))
