from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.utils.timezone import now

from .serializers import *
from custom_user.permissions import *


class CreateApplicationView(APIView):
    serializer_class = ApplicationSerializer

    @swagger_auto_schema(operation_description='creates new application',
                         responses={
                             '200': ApplicationSerializer()
                         })
    def post(self, request):
        ReadyStatus.objects.filter(application__owner=request.user).update(status=False, closed_date=now())
        a = Application.objects.create(owner=request.user)
        ReadyStatus.objects.create(application=a)
        serializer = ApplicationSerializer(a, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetApplicationReadyView(APIView):
    @swagger_auto_schema(operation_description='Returns application by id',
                         responses={
                             '200': ApplicationSerializer(),
                             '400': 'Application does not exist'
                         })
    def get(self, request, app_pk):
        try:
            a = Application.objects.get(id=app_pk, owner=request.user)
        except Application.DoesNotExist:
            return Response('Application does not exist', status=status.HTTP_400_BAD_REQUEST)
        serializer = ApplicationSerializer(a, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CloseApplicationReadyView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    @swagger_auto_schema(operation_description='Close last user\'s application',
                         responses={
                             '200': 'Заявка уже закрыта',
                             '200': ApplicationSerializer(),
                             '400': 'Application does not exist',
                             '400': 'Ready status does not exist',
                             '400': 'KeyError',
                         })
    def post(self, request):
        try:
            a = Application.objects.filter(owner=request.user).last()
            r = a.ready

        except Application.DoesNotExist:
            return Response('Application does not exist', status=status.HTTP_400_BAD_REQUEST)
        except ReadyStatus.DoesNotExist:
            return Response('Ready status does not exist', status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response('KeyError', status=status.HTTP_400_BAD_REQUEST)
        if r.status:
            r.status = False
            r.closed_date = now()
            r.save()
        else:
            return Response('Заявка уже закрыта', status=status.HTTP_200_OK)
        serializer = ApplicationSerializer(a, context={'request': request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class CheckApplicationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ApplicationSerializer
    '''
    DELETE
    '''

    class body1(serializers.Serializer):
        status = serializers.CharField()

    @swagger_auto_schema(operation_description='Check application by id',
                         request_body=body1(),
                         responses={
                             '200': 'Невозможно оценить открытую заявку',
                             '200': ApplicationSerializer(),
                             '400': 'Application does not exist',
                             '400': 'Ready status does not exist',
                             '400': 'KeyError',
                             '400': 'Add correct status',
                         })
    def post(self, request, app_pk):
        d = {
            'accepted': CheckStatus.ACCEPTED,
            'rejected': CheckStatus.REJECTED,
            'revision': CheckStatus.REVISION,
        }

        try:
            a = Application.objects.get(id=app_pk)
            r = a.ready
            if r.status:
                return Response('Невозможно оценить открытую заявку', status=200)
            s = d.get(request.data['status'])

        except Application.DoesNotExist:
            return Response('Application does not exist', status=status.HTTP_400_BAD_REQUEST)
        except ReadyStatus.DoesNotExist:
            return Response('Ready status does not exist', status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response('KeyError', status=status.HTTP_400_BAD_REQUEST)

        if s is None:
            return Response('Add correct status', status=status.HTTP_400_BAD_REQUEST)

        c = CheckStatus.objects.create(status=s,
                                       check_date=now(),
                                       application=a,
                                       judge=request.user)
        if c.status == CheckStatus.REVISION:
            r.status = True
            r.save()
        serializer = ApplicationSerializer(a, context={'request': request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class GetClosedApplicationsView(generics.ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = ApplicationSerializer
    queryset = Application.objects.filter(readystatus__status=False)


class CloseAllApplicationsView(APIView):
    permission_classes = [IsAdmin]

    @swagger_auto_schema(operation_description='Close all applications',
                         responses={
                             '500': 'lol',
                             '200': '',
                         })
    def post(self, request):
        ReadyStatus.objects.filter(status=True).update(status=False, closed_date=now())
        if ReadyStatus.objects.filter(status=True):
            return Response('lol', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK)


class ListOwnApplicationView(generics.ListAPIView):
    queryset = None
    serializer_class = ApplicationSerializer

    def get(self, request):
        self.queryset = Application.objects.filter(owner=request.user).order_by('-id')
        return super().list(request)


class GetIdOfLastApplicationView(APIView):
    '''
    DELETE
    '''

    class body2(serializers.Serializer):
        id = serializers.IntegerField()
        status = serializers.CharField()

    @swagger_auto_schema(operation_description='Get id and status of last app',
                         responses={
                             '500': 'lol',
                             '200': body2(),
                         })
    def get(self, request):
        a = Application.objects.filter(owner=request.user).last()
        data = {
            'id': a.id,
            'status': a.readystatus.status
        }
        return Response(data, status=status.HTTP_200_OK)
