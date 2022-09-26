from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import  IsAuthenticated 
from .models import Comment, Reels , Place
from app import serializers


# to represent reels in homepage

class Homepage(generics.ListCreateAPIView , generics.UpdateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ReelsSerializers
    queryset = Reels.objects.all()

    def get_object(self):
        return self.request

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"status":True,"message":"Updated successfully","data":serializer.data},status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, many=True , context={'request':request})
        return Response({"status":True,"message":"All Reels","data":serializer.data},status=status.HTTP_200_OK)

    def perform_create(self,serializer,user,place):
        serializer.save(user=user , place=place)

    def create(self, request, *args, **kwargs):
        try :
            place = Place.objects.get(id=request.data['place_id'])
        except:
            return Response({'status': False,'message': 'please enter place_id correctly'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer , request.user , place)
        headers = self.get_success_headers(serializer.data)
        return Response({"status":True,"message":"Reels created successfully","data":serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    def patch(self, request, *args, **kwargs):
        return Response({"status":False , "message":"this method not allowed"},status=status.HTTP_400_BAD_REQUEST)





class AddOrDeleteLikeView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            reel = Reels.objects.get(id=request.data['reel_id'])
        except:
            return Response({'status': False,'message': 'Error data (id)' }, status=status.HTTP_400_BAD_REQUEST)
        if self.request.user  not in reel.favourite.all():
            reel.favourite.add(self.request.user)
            return Response({'status': True,'message': 'added successfuly'}, status=status.HTTP_200_OK)
        elif  request.user in reel.favourite.all():
            reel.favourite.remove(request.user)
            return Response({'status': True,'message': 'dish removed from favourite'}, status=status.HTTP_200_OK)
        else :
            return Response({'status': False,'message': 'Error data id'}, status=status.HTTP_400_BAD_REQUEST)




class CommentAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer =  serializers.CommentSerializer

    def post(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request.user)
        return Response({"status":True , "message":"comment added successfully"},status=status.HTTP_201_CREATED)
    
    def delete(self,request,*args, **kwargs):
        try :
            comment_id = Comment.objects.get(id=request.data['comment_id'])
        except :
            return Response({"status":False , "message":"comment_id is incorrect "},status=status.HTTP_400_BAD_REQUEST)
        if comment_id.user == request.user :
            comment_id.delete()
            return Response({"status":True , "message":"comment removed successfully"},status=status.HTTP_204_NO_CONTENT)
        else :
            return Response({"status":False , "message":"you do not have permission "},status=status.HTTP_400_BAD_REQUEST) 





class DecryptAPI(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self,request):
        serializer =serializers.DecreptSerialziers(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"status":True , "message":"null" , "data":serializer.data},status=status.HTTP_202_ACCEPTED)    