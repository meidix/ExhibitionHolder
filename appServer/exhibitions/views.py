from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from exhibitions.models import CoopRequest, Exhibition, Products, Visitor, post_visitor_request_save
from exhibitions.serilializers import CoopRequestSerializer, ExhibitionSerializer, ProductsSerializer, VisitorSerailizer


class ExhibitionViewSet(ModelViewSet):

    queryset = Exhibition.objects.all()
    serializer_class = ExhibitionSerializer
    lookup_filed = 'pk'

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(active=True)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path="all")
    def list_all(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @action(methods=['PUT'], detail=True, url_path="activate")
    def activate(self, request, pk, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=pk)
        except Exhibition.DoesNotExist:
            return Response({ 'error': "the requested exhibition does not exist"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        instance.active = True
        instance.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class VisitorViewSet(ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerailizer
    lookup_field = 'pk'

    def add_m2m_fields(self, instance, *args):
        coops = args[0]
        products = args[1]
        for coop in coops:
            instance.coop_request.add(coop['id'])
        for product in products:
            instance.products_request.add(product['id'])
        return instance

    def create(self, request, pk, *args, **kwargs):
        try:
            exhibition = Exhibition.objects.get(pk=pk)
        except Exhibition.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        coops = data.pop('coop_request', [])
        products = data.pop('product_request', [])
        data['exhibition'] = exhibition.pk
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            instance = self.add_m2m_fields(serializer.instance, coops, products)
            # context = {
            #     "visitor": instance,
            #     'coops': instance.coop_request.all(),
            #     'products': instance.products_request.all(),
            # }
            # subject = f'بازدید کننده جدید در {instance.exhibition.title}'
            # html_message = render_to_string('exhibitions/report.html', context=context)
            # plain_message = strip_tags(html_message)
            # send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [settings.EMAIL_GUEST_USER], fail_silently=True, html_message=html_message)
            post_visitor_request_save.send(sender=Visitor, instance=instance, created=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

class CoopRequestListAPIView(generics.ListAPIView):
    queryset = CoopRequest.objects.all()
    serializer_class = CoopRequestSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer