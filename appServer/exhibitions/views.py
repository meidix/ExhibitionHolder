from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from exhibitions.models import Exhibition, Visitor
from exhibitions.serilializers import ExhibitionSerializer, VisitorSerailizer


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



class VisitorViewSet(ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerailizer
    lookup_field = 'pk'

    def create(self, request, pk, *args, **kwargs):
        try:
            exhibition = Exhibition.objects.get(pk=pk)
        except Exhibition.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['exhibition'] = exhibition.pk
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
