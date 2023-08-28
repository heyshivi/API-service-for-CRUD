from authe.serializer import LogoutSerializer, PasswordResetEmailSerializer, UserPasswordResetSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import status

# Create your views here.

# For creating jwt tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh' : str(refresh),
        'access' : str(refresh.access_token),
    }

#completed
class Registration(APIView):

    def post(self, request, format=None):
        try:
            data_user = {
                'email' : request.data.get('email'),
                'name' : request.data.get('name'),
                'password' : make_password(request.data.get('password')),
                'is_staff' : request.data.get('is_staff'),
                'username':request.data.get('username'),
            }

            serializer = UserSerializer(data = data_user)
            
            if serializer.is_valid():
                user = serializer.save()
                token = get_tokens_for_user(user)

                return Response({"Message" : "Registration Successfull!", "data" : token}, status=status.HTTP_200_OK)
            return Response({"Message" : "Something went wrong!", "data" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Message" : str(e), "data" : None}, status=status.HTTP_400_BAD_REQUEST)

#completed
class login(APIView):

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)
            if user is None:
                return Response({"Message" : "Incorrect Credentials!", "data" : None}, status=status.HTTP_404_NOT_FOUND)

            token = get_tokens_for_user(user)
            return Response({"Message" : "Login Successfull!", "data" : token}, status= status.HTTP_202_ACCEPTED) 
        except Exception as e:
            if type(e) == ValidationError:
                return Response({"Message" : "Please enter correct credentials!", "data" : None}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Message" : str(e), "data" : None}, status=status.HTTP_400_BAD_REQUEST)
#completed
class forgetPassword(APIView):

    def post(self, request):
        try:
            serializer = PasswordResetEmailSerializer(data = request.data)
            if serializer.is_valid(raise_exception=True):
                return Response({"Message" : "Password Reset link send! Please check your email!", "data" : None}, status=status.HTTP_200_OK)
            return Response({"Message" : "Something went wrong!", "data" : serializer.errors}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            if type(e) == ValidationError:
                return Response({"Message" : "Please enter correct credentials!", "data" : None}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Message" : str(e), "data" : None}, status=status.HTTP_400_BAD_REQUEST)

#completed
class UserPasswordReset(APIView):

    def post(self, request, uid, token):
        try:
            serializer = UserPasswordResetSerializer(data=request.data, context = {'uid':uid, 'token':token})
            if serializer.is_valid(raise_exception=True):
                return Response({"Message" : "Password Reset Successfully!", "data" : None}, status=status.HTTP_202_ACCEPTED)
            return Response({"Message" : "Something went wrong!", "data" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            if type(e) == ValidationError:
                return Response({"Message" : "Please enter correct credentials!", "data" : None}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Message" : str(e), "data" : None}, status=status.HTTP_400_BAD_REQUEST)

#completed
class logout(APIView):
       
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            serializer = LogoutSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"Message" : "Logged out successfully!", "data" : None}, status=status.HTTP_202_ACCEPTED)
            return Response({"message": "Please Provide valid Token only!", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            if type(e) == ValidationError:
                return Response({"Message" : "Please enter correct credentials!", "data" : None}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Message" : str(e), "data" : None}, status=status.HTTP_400_BAD_REQUEST)



