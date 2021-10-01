from django_filters import FilterSet, CharFilter, DateTimeFilter
from .models import Post


class PostFilter(FilterSet):

    date = DateTimeFilter(field_name='date', lookup_expr="gte", label='Posted After(DD/MM/YYYY)', input_formats=['%d/%m/%Y'])
    name = CharFilter(field_name='name', lookup_expr="icontains")

    class Meta:
        model = Post
        fields = {'name', 'author'}


