from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *


#user creation
class LeaveRequest(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LeaveApplicationSerializer
    def post(self, request):
        try:
            serializer = LeaveApplicationSerializer(data=request.data)
            if serializer.is_valid():
                print(request.user, 'userrrrr')
                user = User.objects.get(id=request.user.id)
                serializer.validated_data['created_at'] = request.user
                serializer.validated_data['user'] = user
                serializer.validated_data['status'] = "Pending"
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                data = serializer.errors
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except:
            result = {
                "msg":"something went wrong"
            }
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

