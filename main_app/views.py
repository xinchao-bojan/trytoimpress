from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from datetime import datetime

from .serializers import *
from .permissions import *


class CreateApplicationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        r = ReadyStatus.objects.create()
        a = Application.objects.create(owner=request.user,
                                       ready=r)
        serializer = ApplicationSerializer(a, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetApplicationReadyView(APIView):

    def get(self, request, app_pk):
        try:
            a = Application.objects.get(id=app_pk)
        except Application.DoesNotExist:
            return Response('Application does not exist', status=status.HTTP_400_BAD_REQUEST)
        return Response(a.ready.status, status=status.HTTP_200_OK)


class CloseApplicationReadyView(APIView):
    permission_classes = [IsOwner]

    def put(self, request):
        try:
            a = Application.objects.get(owner=request.user)
            r = a.ready

        except Application.DoesNotExist:
            return Response('Application does not exist', status=status.HTTP_400_BAD_REQUEST)
        except ReadyStatus.DoesNotExist:
            return Response('Ready status does not exist', status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response('KeyError', status=status.HTTP_400_BAD_REQUEST)
        if r.status:
            r.status = False
            r.closed_date = datetime.now()
            r.save()
        else:
            return Response('Заявка уже закрыта', status=status.HTTP_200_OK)
        serializer = ApplicationSerializer(a, context={'request': request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class CheckApplicationView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, app_pk):
        try:
            a = Application.objects.get(id=app_pk)
            r = a.ready
            if r.status:
                return Response('Невозможно оценить открытую заявку')
            c = CheckStatus.objects.create(status=request.data['status'],
                                           check_date=datetime.now(),
                                           application=a)
        except Application.DoesNotExist:
            return Response('Application does not exist', status=status.HTTP_400_BAD_REQUEST)
        except ReadyStatus.DoesNotExist:
            return Response('Ready status does not exist', status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response('KeyError', status=status.HTTP_400_BAD_REQUEST)

        if c.status is 'rejected':
            r.status = True
            r.save()
        serializer = ApplicationSerializer(a, context={'request': request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class GetClosedApplicationsView(APIView):
    permission_classes = [IsAdmin]
    serializer_class = ApplicationSerializer
    queryset = Application.objects.filter(ready__status=False)
