from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from app.account.api.permissions import IsOwnerReadOnly
# from app.account.api.permissions import IsOwnUserOrReadOnly
from app.account.api.serializer import RegisterSerializer, LoginSerializer, MyProfileSerializer, AccountUpdateSerializer
from app.account.models import Account


class AccountRegisterView(generics.GenericAPIView):
    # http://127.0.0.1:8000/account/api/register/
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        print(user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # user_data = serializer.data
        # email = serializer.data.get('email')
        # tokens = Account.objects.get(email=email).tokens
        # user_data['tokens'] = tokens
        return Response({'success': True, 'data': "Account Successfully Created"}, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    # http://127.0.0.1:8000/account/api/login/
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"tokens" :serializer.data['tokens']}, status=status.HTTP_200_OK)
        #return Response({'success': True, 'tokens': serializer.data['tokens']}, status=status.HTTP_200_OK)


class MyProfileView(generics.GenericAPIView):
    # http://127.0.0.1:8000/account/api/my_profile/
    serializer_class = MyProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Account.objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user)
        return Response({"success": True, 'data': serializer.data}, status=status.HTTP_200_OK)


class AccountRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    # http://127.0.0.1:8000/account/api/retrieve-update/<pk>
    serializer_class = AccountUpdateSerializer
    queryset = Account.objects.all()
    permission_classes = (IsOwnerReadOnly, IsAuthenticated)

    def get(self, request, *args, **kwargs):
        query = self.get_object()
        if query:
            serializer = self.get_serializer(query)
            return Response({"success": True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'query did not exit'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'credentials is invalid'}, status=status.HTTP_404_NOT_FOUND)