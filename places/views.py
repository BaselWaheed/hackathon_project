from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import  IsAuthenticated 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from app.models import Reels
from app.serializers import ReelsSerializers
from accounts.serializers import UserSerializers
from .models import Place
from .serializers import PlaceSerializers


class UserDetailsAPI(generics.RetrieveAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ReelsSerializers

    def get_object(self):
        obj = Reels.objects.filter(user=self.request.user)
        return obj

    def retrieve(self, request, *args, **kwargs):
        list_1 = {"profile":{},"reels":[]}
        instance = self.get_object()
        serializer= self.get_serializer(instance , many=True , context={'request':request})
        serializer_1 =  UserSerializers(request.user)
        list_1["profile"] = serializer_1.data
        list_1["reels"] = serializer.data 
        return Response({"status":True,"message":("profile"),"data":list_1}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)






class SearchAPI(generics.ListAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Reels.objects.all()
    serializer_class = ReelsSerializers
    filter_backends = [DjangoFilterBackend ,filters.SearchFilter]
    filterset_fields = ['place__category__cat_name']
    search_fields = ['place__place_name']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status":True,"message":"null","data":serializer.data},status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PlacesAPI(generics.ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Place.objects.all()
    serializer_class = PlaceSerializers

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status":True,"message":"null","data":serializer.data},status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)