# this came from https://djangosnippets.org/snippets/2196/
# adds a collect tag for templates so you can build lists

from django import template
from django.contrib import admin
from django.contrib.gis.geos import GEOSGeometry
from django.core.management import settings

register = template.Library()


@register.tag
def collect(token):
    bits = list(token.split_contents())
    if len(bits) > 3 and bits[-2] == 'as':
        varname = bits[-1]
        items = bits[1:-2]
        return CollectNode(items, varname)
    else:
        raise template.TemplateSyntaxError('%r expected format is "item [item ...] as varname"'
                                           % bits[0])


class CollectNode(template.Node):
    def __init__(self, items, varname):
        self.items = map(template.Variable, items)
        self.varname = varname

    def render(self, context):
        context[self.varname] = [i.resolve(context) for i in self.items]
        return ''


class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''


def do_assign(parser, token):
    """
    Assign an expression to a variable in the current context.

    Syntax::
        {% assign [name] [value] %}
    Example::
        {% assign list entry.get_related %}

    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)


register = template.Library()
register.tag('assign', do_assign)


# Extra template tags for map
@register.filter()
def get_lat_lng(value, gc):
    lat = GEOSGeometry(value).coords[1]
    lon = GEOSGeometry(value).coords[0]

    if gc == 'lat':
        return "{}".format(lat)
    elif gc == 'lon':
        return "{}".format(lon)


@register.filter()
def filter_coords(value):
    sites = list()
    for site in value:
        lat = GEOSGeometry(site.featuregeometry).coords[1]
        lon = GEOSGeometry(site.featuregeometry).coords[0]
        if lat != 0 and lon != 0:
            sites.append(site)

    return sites


@register.filter()
def get_title(value, short):
    if value == 'site_title':
        return admin.site.site_title
    elif value == 'site_header':
        return admin.site.site_header
    elif value == 'shortcut_title':
        return settings.ADMIN_SHORTCUTS[0]['shortcuts'][short]['title']


@register.filter()
def in_field(value):
    val = value.split(" ")
    return val[0]



# settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")

# https://stackoverflow.com/questions/771890/how-do-i-get-the-class-of-a-object-within-a-django-template
@register.filter(name='get_class')
def get_class(value):
  return value.__class__.__name__