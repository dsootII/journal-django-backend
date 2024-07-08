from django.shortcuts import render
from rest_framework import generics, viewsets, response
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from loginlearnapi.settings import JWT_SECRET
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import AllowAny
# Create your views here.
def get_user_from_auth_header(request):
  token = request.headers['Authorization']
  token = token.split()[1]
  
  if not token:
    raise AuthenticationFailed('unauthnenticated request')  
  user_details = jwt.decode(token, JWT_SECRET, algorithms='HS256')
  try:
    user = User.objects.filter(id=user_details['user_id']).first()
  except Exception as e:
    raise AuthenticationFailed('internal server error')
  if not user:
    raise AuthenticationFailed('invalid token')
  return user

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  
  if not refresh:
    raise AuthenticationFailed("Authentication failed.")

  return {
    'refresh': str(refresh),
    'access': str(refresh.access_token),
  }

class SignupView(APIView):  
  def post(self, request):
    serializer = UserSerializer(data=request.data)
    try:
      if serializer.is_valid():
        user = serializer.save()
        print(user)
        return Response(get_tokens_for_user(user=user))
      else:
        return response.Response({"errors": serializer.errors})    
    
    except Exception as e:
      print(e)
      return response.Response({"msg": "error occured"})

class LoginView(APIView):
  def post(self, request):
    provided_username = request.data['username']
    provided_password = request.data['password']
    
    user = User.objects.filter(username=provided_username).first()
    print("user found ", user);
    if user is None:
      raise AuthenticationFailed("User not found")
    if not user.check_password(provided_password):
      raise AuthenticationFailed("Incorrect Password")
    
    return Response(get_tokens_for_user(user))

class UserView(APIView):
  def get(self, request):
    user = get_user_from_auth_header(request=request)
    containers = Container.objects.filter(user=user)
    return Response({
      "user": UserSerializer(user).data,
      "containers": ContainerSerializer(containers, many=True).data
    })

class LogoutView(APIView):
  def get(self, request):
    token = request.headers['Authorization']
    token = token.split()[1]
    if not token:
      raise AuthenticationFailed('unauthnenticated request')
    
    # res.delete_cookie(key='token')
    #since we're using jwt, there's no logging out as such on the backend. 
    #on the frontend, have to delete that token from the localStorage. 
    return Response({"detail" :"you're logged out"})

#for a user to access their containers. 
class ContainerListView(generics.ListAPIView):
  # queryset = Container.objects.all()
  # serializer_class = ContainerSerializer
  # permission_classes = [AllowAny]
  
  def get(self, request):
    user = get_user_from_auth_header(request=request)
    containers = Container.objects.all().filter(user=user.pk)
    serializer = ContainerSerializer(containers, many=True)
    return Response(serializer.data)
    
# class ContainerListView(APIView):
#   def get(self, request):
#         containers = Container.objects.all()
#         try:
#           serializer = ContainerSerializer(containers, many=True)
#           print(serializer)
#           print(serializer.data)
#           if serializer.is_valid():
#             print(serializer.data)
#           return response.Response(serializer.data)
#         except Exception as e:
#           print("exception occured, ", e)
#           return response.Response(serializer.errors)
  
class ContainerCreateView(generics.CreateAPIView):
  print('container create view entered')
  queryset = Container.objects.all()
  serializer_class = ContainerSerializer
  
class ContainerDeleteView(generics.DestroyAPIView):
  queryset = Container.objects.all()
  serializer_class = ContainerSerializer
  
class EditContainerView(APIView):
    def patch(self, request, pk):
        container = Container.objects.get(pk=pk)
        serializer = ContainerSerializer(container, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
  
class EntryViewSet(viewsets.ModelViewSet):
  queryset = Entry.objects.all()
  serializer_class = EntrySerializer
  permission_classes = [AllowAny]

