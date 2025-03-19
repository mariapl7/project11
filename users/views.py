from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class UserPaymentHistorySerializer:
    pass


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user  # Получаем текущего аутентифицированного пользователя
        serializer = UserPaymentHistorySerializer(user)
        return Response(serializer.data)
