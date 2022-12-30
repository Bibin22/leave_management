from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *


#user creation
class UserRegistration(APIView):
    serializer_class = UserRegisterSerializer
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        print(request.user.is_superuser)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Registrations Sucessfull"
            data['username'] = account.username
            data['email'] = account.email
            data['token'] = Token.objects.get(user=account).key
        else:
            data = serializer.errors
            return Response(data)
        return Response(data, status=status.HTTP_201_CREATED)


#logout

class LogOut(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


#Manage Employee Details
class EditEmployee(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeEditSerializer

    def get(self, request, id):
        try:
            if request.user.is_superuser:
                user = User.objects.get(id=id)
                results = {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,

                }
                return Response(results, status=status.HTTP_200_OK)
            else:
                results = {
                    "msg":"only superuser can edit employee details"
                }
                return Response(results, status=status.HTTP_401_UNAUTHORIZED)
        except:
            results = {
                "msg": "something went wrong"
            }
            return Response(results, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            if request.user.is_superuser:
                user = User.objects.get(id=id)
                serializer = EmployeeEditSerializer(user, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    data = serializer.errors
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                results = {
                    "msg": "only superuser can edit employee details"
                }
                return Response(results, status=status.HTTP_401_UNAUTHORIZED)

        except:
            results = {
                "msg": "something went wrong"
            }
            return Response(results, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            if request.user.is_superuser:
                User.objects.get(id=id).delete()
                result = {
                    "msg":"user deleted"
                }
                return Response(result, status=status.HTTP_204_NO_CONTENT)
            else:
                results = {
                    "msg": "only superuser can edit employee details"
                }
                return Response(results, status=status.HTTP_401_UNAUTHORIZED)
        except:
            results = {
                "msg": "something went wrong"
            }
            return Response(results, status=status.HTTP_400_BAD_REQUEST)


