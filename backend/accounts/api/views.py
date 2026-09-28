from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.text import slugify

from accounts.api.serializers import UserSerializer, RegisterSerializer, LoginSerializer
from accounts.models import User
from tenants.models import Tenant, TenantMember
from profiles.models import UserProfile


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Automatically provision initial workspace Tenant and UserProfile
            tenant_slug = slugify(f"{user.first_name or 'workspace'}-{str(user.id)[:8]}")
            tenant, _ = Tenant.objects.get_or_create(
                owner=user,
                defaults={'name': f"{user.full_name}'s Career Space", 'slug': tenant_slug}
            )
            TenantMember.objects.get_or_create(
                tenant=tenant,
                user=user,
                defaults={'role': TenantMember.Role.OWNER}
            )
            UserProfile.objects.get_or_create(
                user=user,
                tenant=tenant,
                defaults={
                    'headline': 'Full Stack / Python / React Software Engineer',
                    'remote_preference': UserProfile.WorkPreference.REMOTE,
                    'profile_completion': 75
                }
            )

            # Generate real JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'message': 'User registered successfully.',
                'data': {
                    'user': UserSerializer(user).data,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }
            }, status=status.HTTP_201_CREATED)
            
        return Response({
            'success': False,
            'message': 'Validation failed.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'success': True,
                    'message': 'Login successful.',
                    'data': {
                        'user': UserSerializer(user).data,
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                    }
                })
            return Response({
                'success': False,
                'message': 'Invalid email or password.'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        return Response({
            'success': False,
            'message': 'Validation failed.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileMeView(APIView):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            # Fallback for dev exploration if unauthenticated
            first_user = User.objects.first()
            if first_user:
                user = first_user
            else:
                return Response({'success': False, 'message': 'Unauthenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_data = UserSerializer(user).data
        # Attach tenant if exists
        tenant_member = TenantMember.objects.filter(user=user).select_related('tenant').first()
        if tenant_member:
            user_data['tenant'] = {
                'id': str(tenant_member.tenant.id),
                'name': tenant_member.tenant.name,
                'role': tenant_member.role,
            }
        
        return Response({
            'success': True,
            'data': user_data
        })
