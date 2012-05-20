class ModelChannelBackendMixin(object):
    """
    A trivial implementation of the channel backend methods.

    model
        The model class this channel serves. If None, a new class will be
        created in registry.register, and the model attribute will be set in
        that subclass. So you probably don't need to worry about it, just know
        that it's there for you to use.

    search_field
        The name of the field that the default implementation of query_filter
        uses. Default is 'name'.
    """

    model = None
    search_field = 'name'

    def query_filter(self, results):
        """
        Filter results using the request.

        By default this will expect results to be a queryset, and will filter
        it with self.search_field + '__icontains'=self.request['q'].
        """
        q = self.request.GET.get('q', None)

        if q:
            kwargs = {"%s__icontains" % self.search_field: q}
            results = results.filter(**kwargs)

        return results

    def values_filter(self, results, values):
        """
        Filter results based on a list of values.

        By default this will expect values to be an iterable of model ids, and
        results to be a queryset. Thus, it will return a queryset where pks are
        in values.
        """
        results = results.filter(pk__in=values)
        return results

    def get_queryset(self):
        """
        Return a queryset for the channel model.
        """
        return self.model.objects.all()

    def get_results(self, values=None):
        """
        Return an iterable of result to display in the autocomplete box.

        By default, it will:

        - call self.get_queryset(),
        - call values_filter() if values is not None,
        - call query_filter() if self.request is set,
        - call order_results(),
        - return a slice from offset 0 to self.limit_results.
        """
        results = self.get_queryset()

        if values is not None:
            # used by the widget to prerender existing values
            results = self.values_filter(results, values)

        elif self.request:
            # used by the autocomplete
            results = self.query_filter(results)

        return self.order_results(results)[0:self.limit_results]

    def order_results(self, results):
        """
        Return the result list after ordering.

        By default, it expects results to be a queryset and order it by
        search_field.
        """
        return results.order_by(self.search_field).distinct()

    def are_valid(self, values):
        """
        Return True if the values are valid.

        By default, expect values to be a list of object ids, return True if
        all the ids are found in the queryset.
        """
        return self.get_queryset().filter(pk__in=values).count() == len(values)


