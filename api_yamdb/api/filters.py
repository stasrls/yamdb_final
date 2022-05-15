from django_filters import CharFilter, rest_framework

from reviews.models import Title


class TitleFilter(rest_framework.FilterSet):
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('name', 'year', 'category__slug', 'genre__slug')
