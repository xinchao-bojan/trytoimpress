from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.utils.timezone import now

from .serializers import *
from custom_user.permissions import *


class CreateApplicationView(APIView):

    def post(self, request):
        try:
            Application.objects.get(owner=request.user)
            return Response('already exist', status=status.HTTP_400_BAD_REQUEST)
        except Application.DoesNotExist:
            a = Application.objects.create(owner=request.user)
            ReadyStatus.objects.create(application=a)
            serializer = ApplicationSerializer(a, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetApplicationReadyView(APIView):

    def get(self, request, app_pk):
        try:
            a = Application.objects.get(id=app_pk)
        except Application.DoesNotExist:
            return Response('Application does not exist', status=status.HTTP_400_BAD_REQUEST)
        serializer = ApplicationWODateSerializer(a, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CloseApplicationReadyView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request):
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
            r.closed_date = now()
            r.save()
        else:
            return Response('Заявка уже закрыта', status=status.HTTP_200_OK)
        serializer = ApplicationSerializer(a, context={'request': request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class CheckApplicationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

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
                return Response('Невозможно оценить открытую заявку')
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
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ApplicationSerializer
    queryset = Application.objects.filter(readystatus__status=False)
