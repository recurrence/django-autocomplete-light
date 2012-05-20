from django.template import loader

class TemplateChannelFrontendMixin(object):
    """
    A trivial implementation of a channel frontend methods using templates.

    Attributes:

    result_template
        The template to use in result_as_html method, to render a single
        autocomplete suggestion. By default, it is
        autocomplete_light/channelname/result.html or
        autocomplete_light/result.html.

    autocomplete_template
        The template to use in render_autocomplete method, to render the
        autocomplete box. By default, it is
        autocomplete_light/channelname/autocomplete.html or
        autocomplete_light/autocomplete.html.
    """
    
    result_template = None
    autocomplete_template = None

    def __init__(self):
        """
        Set result_template and autocomplete_template if necessary.
        """
        if not self.result_template:
            self.result_template = [
                'autocomplete_light/%s/result.html' % self.__class__.__name__.lower(),
                'autocomplete_light/result.html',
            ]

        if not self.autocomplete_template:
            self.autocomplete_template = [
                'autocomplete_light/%s/autocomplete.html' % self.__class__.__name__.lower(),
                'autocomplete_light/autocomplete.html',
            ]

    def result_as_html(self, result):
        """
        Return the html representation of a result for display in the deck
        and autocomplete box.

        By default, render result_template with channel and result in the
        context.
        """
        return loader.render_to_string(self.result_template, {
            'channel': self,
            'result': result,
        })

    def render_autocomplete(self):
        """
        Render the autocomplete suggestion box.

        By default, render self.autocomplete_template with the channel in the
        context.
        """
        return loader.render_to_string(self.autocomplete_template, {
            'channel': self,
        })
