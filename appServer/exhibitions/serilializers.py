from django_jalali.db.models import jDateField
from rest_framework.serializers import ModelSerializer
from django_jalali.serializers.serializerfield import JDateField

from .models import Exhibition, Visitor, CoopRequest, Products

class ExhibitionSerializer(ModelSerializer):
    start_date = JDateField()
    end_date = JDateField()

    class Meta:
        model = Exhibition
        exclude = []


class VisitorSerailizer(ModelSerializer):

    class Meta:
        model = Visitor
        exclude = []
        extra_kwargs = {
            'exhibition': { 'write_only': True}
        }

class CoopRequestSerializer(ModelSerializer):

    class Meta:
        model = CoopRequest
        exclude = ['visitor']


class ProductsSerializer(ModelSerializer):

    class Meta:
        model = Products
        exclude = ['visitor']