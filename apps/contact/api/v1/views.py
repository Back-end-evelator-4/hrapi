from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, AllowAny

from apps.contact.models import Contact
from .filters import ContactFilter
from .serializers import ContactSerializer


class ContactListAPIView(ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAdminUser]
    filterset_class = ContactFilter

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.GET.get('is_deleted'):
            return qs.filter(is_deleted=False)
        return qs.filter(is_deleted=True)

class ContactCreateAPIView(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]


class ContactRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()



