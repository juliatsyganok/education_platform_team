from django_filters import rest_framework as filters
from .models import Course
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset

class CoursesFilter(filters.FilterSet):
    price=filters.RangeFilter(field_name='price')

    class Meta:
        model=Course 
        fields=['price']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.add_input(Reset('reset', 'Очистить'))
    #     self.helper.add_input(Submit('submit', 'Фильтровать'))