from functools import wraps
import jwt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse


def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token


def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """

    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            decoded = jwt.decode(token, verify=False)
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse({'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response

        return decorated

    return require_scope


@api_view(['GET'])
@permission_classes([AllowAny])
def public(request):
    return JsonResponse({'message': 'Hello from a public endpoint! You don\'t need to be authenticated to see this.'})


@api_view(['GET'])
def private(request):
    return JsonResponse({'message': 'Hello from a private endpoint! You need to be authenticated to see this.'})


from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView

from .permissions import *
from .serializers import *


class GivePositionView(generics.ListAPIView):
    permission_classes = [IsAdmin]
    queryset = None
    serializer_class = CustomUserPositionSerializer

    def get(self, request):
        self.queryset = CustomUser.objects.all()
        return super().list(request)

    def put(self, request):
        try:
            p, created = Position.objects.get_or_create(position=request.data['position'])
            u = CustomUser.objects.get(pk=request.data['user'])
        except KeyError:
            return Response('KeyError', status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response('Custom user does not exist', status=status.HTTP_400_BAD_REQUEST)
        u.position.add(p)
        serializer = CustomUserPositionSerializer(u, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListUserRoles(generics.ListAPIView):

    def get(self, request):
        serializer = PositionSerializer(Position.objects.filter(customuser=request.user), many=True,
                                        context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
