# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

from django.contrib import admin
from django.core.management import settings

from odm2admin.models import Samplingfeatures


class SamplingFeatureTypeListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Sampling Feature Type'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'sampling_feature_type'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_of_types = []
        queryset = Samplingfeatures.objects.all()
        featuretypes = list(set(queryset.values_list('sampling_feature_type', flat=True)))
        for sf in featuretypes:
            list_of_types.append(
                (sf, sf)
            )
        return sorted(list_of_types, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value():
            return queryset.filter(sampling_feature_type=self.value())

        return queryset