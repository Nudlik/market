import django_filters
from django.db.models import Q

from ads.models import Ad


class AdFilerSet(django_filters.rest_framework.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    title_or_description = django_filters.CharFilter(
        method='title_or_description_',
        label='Поиск по заголовку или описанию'
    )
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Ad
        fields = ['title', 'title_or_description']

    def title_or_description_(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))
