"""
The channel.base module provides a channel class which you can extend to make
your own channel. It also serves as default channel class.
"""

from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _

__all__ = ('ChannelBase',)


class ChannelBase(object):
    """
    A basic implementation of a channel, which should fit most use cases.

    Attributes:

    limit_results
        The number of results that this channel should return. For example, if
        query_filter returns 50 results and that limit_results is 20, then the
        first 20 of 50 results will be rendered. Default is 20.

    bootstrap
        The name of the bootstrap kind. By default, deck.js will only
        initialize decks for wrappers that have data-bootstrap="normal". If
        you want to implement your own bootstrapping logic in javascript,
        then you set bootstrap to anything that is not "normal". Default is
        'normal'.

    placeholder
        The initial text in the autocomplete text input.
    
    static_list
        A list of static files which are necessary for this channel. It is an
        empty list by default.
    
    request
        When javascript queries for the autocomplete box that matches a search
        string, this attribute is set by init_for_request()
    """

    limit_results = 20
    bootstrap = 'normal'
    placeholder = _(u'type some text to search in this autocomplete')
    static_list = []
    request = None

    def get_absolute_url(self):
        """
        Return the absolute url for this channel, using
        autocomplete_light_channel url
        """
        return urlresolvers.reverse('autocomplete_light_channel', args=(
            self.__class__.__name__,))

    def as_dict(self):
        """
        Return a dict of variables for this channel, it is used by javascript.
        """
        return {
            'url': self.get_absolute_url(),
            'name': self.__class__.__name__
        }

    def init_for_request(self, request, *args, **kwargs):
        """
        Set self.request, self.args and self.kwargs, useful in query_filter.
        """
        self.request = request
        self.args = args
        self.kwargs = kwargs
