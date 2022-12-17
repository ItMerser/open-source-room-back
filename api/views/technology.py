from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK

from core.models import Language, Technology


class LanguagesListApiView(APIView):
    def get(self, request):
        languages = list(Language.objects.all().values_list('name', flat=True))
        return Response(status=HTTP_200_OK, data=languages)


class TechnologiesListApiView(APIView):
    def get(self, request):
        technologies = list(Technology.objects.all().values('name', 'type'))
        return Response(status=HTTP_200_OK, data=technologies)
