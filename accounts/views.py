from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import  IsAuthenticated , AllowAny
from accounts import serializers
from .email import email_verify, generate_code , reset_password
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import jwt
from django.contrib.auth import login 
from rest_framework.renderers import TemplateHTMLRenderer
from .models import User
from twilio.rest import Client
from decouple import Config


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self , request):
        serializer = serializers.RegisterSerialzier(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_verify(request,user)
        return Response({"status":True , "message":"please check your mail to activate account"} , status=status.HTTP_200_OK)





#verify user by link activate
class VerifyEmail(APIView):

    serializer_class = serializers.EmailVerificationSerializer
    renderer_classes = [TemplateHTMLRenderer]
    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self , request , **kwargs):
        token = request.GET.get('token')

        try :
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({ 'status' : True ,'message' :'Congratolations  Your Email is Activated'},template_name='email_verified.html',status=status.HTTP_200_OK)
            return Response({ 'status' : False ,'message' :'Error'},template_name='error404.html',status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({ 'status' : False ,'message' :'Activation Link Expired'} ,template_name='email_failed.html',status=status.HTTP_400_BAD_REQUEST)

        except jwt.DecodeError as identifier:
            return Response({ 'status' : False ,'message' :'Token invalid'} ,template_name='error404.html',status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):

    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request,user)
        data = {
            "first_name" :user.first_name ,
            "last_name" : user.last_name , 
            "email" : user.email ,
            "username" : user.username,
            "phone_number" : str(user.phone_number) ,
            "access" : user.get_tokens_for_user()['access'],
            "refresh" : user.get_tokens_for_user()['refresh'],
        }
        return Response({
            'status': True, "message": 'Login successfully' ,  "data":data
        }, status=status.HTTP_200_OK)


class AddPhone(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = serializers.PhoneNumberSerializer
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        serializer = self.serializer_class(request.user,data=request.data )
        serializer.is_valid(raise_exception=True)
        code = generate_code()
        user = serializer.save(code=code)
        account_sid = Config('TWILIO_ACCOUNT_SID')
        auth_token = Config('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        message = client.messages.create(
                body=f"Hackathon Backend\n you can verify phonenumber by the code {code}",
                from_=Config('phone_number'),
                to= request.data["phone_number"]
                )

        return Response({"status":True , "message":"the code sent to "+request.data['phone_number']},status=status.HTTP_202_ACCEPTED)


class ChangePasswordView(generics.GenericAPIView):
    authentication_classes = (JWTAuthentication,)  
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PasswordChangeSerializer


    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():   
            user = request.user
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            confermation_password = request.data.get('confermation_password')
            if confermation_password != new_password :
                return Response({'status' : False,'message': 'password bot match'}, status=status.HTTP_200_OK)
            if not user.check_password(old_password):
                return Response({'status' : False,'message': 'password in correct'}, status=status.HTTP_200_OK)
            user.set_password(new_password)
            user.save()
            return Response({'status' : True,'success': 'Password changed'}, status=status.HTTP_200_OK)
        return Response({'status' : False,'messege': 'Password incorrect'}, status=status.HTTP_400_BAD_REQUEST)


class SendpasswordResetEmail(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = serializers.ResetPassword
    def post(self,request,format=None):
        serializer = self.get_serializer(data =request.data)
        serializer.is_valid(raise_exception=True)
        reset_password(request.data['email'])
        return Response({'status': True,'messege' : 'check your email'},status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    
    serializer_class = serializers.LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)






