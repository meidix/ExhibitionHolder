from django_jalali.db.models import jDateField
from rest_framework.serializers import ModelSerializer
from django_jalali.serializers.serializerfield import JDateField

from .models import Exhibition, Visitor

class ExhibitionSerializer(ModelSerializer):
    start_date = JDateField()
    end_date = JDateField()

    class Meta:
        model = Exhibition
        exclude = ['form_header']


class VisitorSerailizer(ModelSerializer):

    class Meta:
        model = Visitor
        exclude = []
        extra_kwargs = {
            'exhibition': { 'write_only': True}
        }