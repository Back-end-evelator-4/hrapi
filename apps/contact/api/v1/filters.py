from django_filters import FilterSet
from apps.contact.models import Contact


class ContactFilter(FilterSet):
    class Meta:
        model = Contact
        fields = ['is_deleted']
