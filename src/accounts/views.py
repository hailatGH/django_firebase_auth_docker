from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Permission, Group
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated, IsAdminUser

from .models import CustomUser
from .serializers import UserSerializer, GroupSerializer, PermissionSerializer

import json
from rest_framework.views import APIView
from rest_framework.response import Response
from firebase_admin import auth
from .models import CustomUser

class UserSignIpView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            login = auth.sign_in_with_email_and_password(email, password)
            token = login['refreshToken']
            print(token)
            Response(f"{token}")
        except BaseException as e:
            print(e)
            return Response("Falied")
        # try:
        #     # Sign in the user using Firebase Authentication
        #     user = auth.get_user_by_email(email)
        #     uid = user.uid
        #     print(json(user))
        #     # auth.verify_password(uid=uid, password=password)

        #     # Generate a Firebase ID token for the user
        #     token = auth.create_custom_token(uid)

        #     # Return the token in the response
        #     return Response({'token': token})

        # except BaseException as error:
        #     return Response({'error': f'{error}'})

class UserSignUpView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        # return Response(f"{email} - {password}")
        try:
            user = auth.create_user(
                email=email,
                password=password,
            )
            print(user.uid)
            print(user.email)
            custom_user = CustomUser.objects.create(uid=str(user.uid).strip(), email=email)
            return Response({'message': 'User created successfully'})
        except BaseException as error:
            return Response({'message': 'Failed to create user', 'error': f"{error}"})
        

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated, DjangoModelPermissions]
    
    def create(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.add_customuser'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.change_customuser'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.view_customuser'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().retrieve(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.view_customuser'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().list(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.delete_customuser'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().destroy(request, *args, **kwargs)

class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer
    permission_classes=[DjangoModelPermissions, IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.add_group'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.change_group'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.view_group'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().retrieve(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.view_group'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().list(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.delete_group'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().destroy(request, *args, **kwargs)

class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all().order_by('id')
    serializer_class = PermissionSerializer
    permission_classes=[DjangoModelPermissions, IsAuthenticated, IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.add_permission'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.change_permission'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.view_permission'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().retrieve(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.view_permission'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().list(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.delete_permission'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().destroy(request, *args, **kwargs)