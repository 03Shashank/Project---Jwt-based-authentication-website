from rest_framework import response
from rest_framework.exceptions import AuthenticationFailed
from home import serializers
from django.shortcuts import render,redirect
from datetime import datetime
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import check_password
# from rest_framework import serializers
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt, datetime
from rest_framework.renderers import TemplateHTMLRenderer



# # Create your views here.
token = ""

def index(request):
     if request.user.is_anonymous:
          return render(request,'login-signup.html')
     return render(request,'update_user.html')

class registerview(APIView):
     def post(self,request):
          serializer = serializers.UserSerializer(data = request.data)
          serializer.is_valid(raise_exception=True)
          
          Rpassword = request.data['password']
          Rre_password = request.data["re-enteredpassword"]
          # print(Rre_password)
          if Rpassword!=Rre_password:
               messages.warning(request, "ERROR: Password and Re-Entered Password does not Match. Please SignUp again.")
               return render(request,'login-signup.html')
          
          serializer.save()
     
          messages.success(request,"Account registered")
          return render(request,'login-signup.html')
     
class LoginView(APIView):

     def post(self,request):
          email = request.data['email']
          password = request.data['password']

          user = User.objects.filter(email=email).first()

          

          if user is None:
               raise AuthenticationFailed("user not found")

          if not user.check_password(password):
               raise AuthenticationFailed("user not found")

          

          payload = {
               'id': user.id,
               "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes = 5),
               'iat': datetime.datetime.utcnow()

               }

          global token
          token = jwt.encode(payload, 'secret',algorithm='HS256').decode('utf-8')

          

          response1 = Response()
          
          # print("current -------------------- ", token)

          response1.set_cookie(key = 'jwt' , value= token, httponly =True)

          response1.data = {
               'jwt': token
          }

          return redirect("/api/userv")
 
     
class UserView(APIView):

     renderer_classes = [TemplateHTMLRenderer]
     template_name = 'update_user.html'
     print("0")

     def get(self,request):

          global token
          print(token)

          if not token:
               
               raise AuthenticationFailed('Unauthenticated')
          
          try:
               
               payload = jwt.decode(token, 'secret', algorithm = ['HS256'])
               
     
          except jwt.ExpiredSignatureError:
               
               raise AuthenticationFailed('Unauthenticated')


          user = User.objects.filter(id = payload['id']).first()
          serializer = serializers.UserSerializer(user)

          return render(request,'update_user.html' , {'user':user})

class LogoutView(APIView):
     def get(self,request):
          global token
          token = ""
          response = Response()
          response.delete_cookie('jwt')
          return redirect("/api/index")


class updateuser(APIView):
     def post(self,request):
          global token
          print(token)
          try:
               payload = jwt.decode(token, 'secret', algorithm = ['HS256'])
     
          except jwt.ExpiredSignatureError:
               raise AuthenticationFailed('Unauthenticated')

          user = User.objects.filter(id = payload['id']).first()


          print(user.first_name)

          Uemail = request.data['update_email']
          Ufname = request.data['update_first_name']
          Ulname = request.data['update_last_name']
          Uaddress = request.data['update_address']
          confirm_password = request.data["confirm_password"]

          real_password = user.password

          print("1st-------------------------------------------------")
          print(real_password)
          print(confirm_password)
          print(check_password(confirm_password,real_password))
          if not check_password(confirm_password,real_password):
               print("2ndt--------")
               messages.warning(request, "ERROR: Password does not Match current password. Please enter the correct password.")
               return redirect("/api/userv")
          else:
               print("3rd--------")
               if Uemail!= "":
                    user.email = Uemail
               if Ufname != "":
                    user.first_name = Ufname  
               if Ulname != "":
                    user.last_name = Ulname

               if Uaddress != "":
                    user.Address = Uaddress
     
               user.save()
          print(user.first_name)
          print("4th--------")
          messages.success(request, "Profile Updated succesfully!")
          return render(request,'update_user.html' , {'user':user})


def delete_user(request):
     global token
     print(token)
     try:
          payload = jwt.decode(token, 'secret', algorithm = ['HS256'])
     except jwt.ExpiredSignatureError:
          raise AuthenticationFailed('Unauthenticated')

     user = User.objects.filter(id = payload['id']).first()

     user.delete()
     token = ""
     messages.warning(request, "The user is deleted")
     return redirect("/api/index")