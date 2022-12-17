from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView

from api.serializers.specialist import (
    SpecialistSerializer,
    SpecialistCreationSerializer,
    SpecialistAuthenticationSerializer,
    SpecialistUpdatingSerializer,
)
from api.validators import validate_password
from core.models import Specialist, Language, Technology


class SpecialistsListApiView(APIView):
    def get(self, request):
        specialists = Specialist.objects.prefetch_related('languages', 'technologies', 'projects')
        serializer = SpecialistSerializer(specialists, many=True)
        return Response(status=HTTP_200_OK, data=serializer.data)


class SpecialistRetrieveApiView(APIView):
    def get(self, request, specialist_id: str):
        try:
            specialist = Specialist.objects.prefetch_related(
                'languages', 'technologies', 'projects'
            ).get(pk=specialist_id)
        except Specialist.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        serializer = SpecialistSerializer(specialist)
        return Response(status=HTTP_200_OK, data=serializer.data)


class SpecialistCreationApiView(APIView):
    def post(self, request):
        serializer = SpecialistCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        specialist = serializer.save()

        token = Token.objects.get(user=specialist)

        specialist = SpecialistSerializer(specialist)
        response_data = {
            **specialist.data,
            'token': token.key,
        }
        return Response(status=HTTP_201_CREATED, data=response_data)


class SpecialistAuthenticationApiView(APIView):
    def post(self, request):
        serializer = SpecialistAuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            specialist = Specialist.objects.get(nickname=serializer.validated_data['nickname'])
        except Specialist.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        token = Token.objects.get(user=specialist)
        specialist = SpecialistSerializer(specialist)
        response_data = {
            **specialist.data,
            'token': token.key,
        }
        return Response(status=HTTP_200_OK, data=response_data)


class SpecialistUpdatingApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def patch(self, request):
        serializer = SpecialistUpdatingSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_200_OK)


class SpecialistUpdatingPasswordApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def patch(self, request):
        new_password = request.data.get('password')
        if new_password and validate_password(password=new_password):
            specialist = request.user
            specialist.set_password(new_password)
            specialist.save()
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class SpecialistLanguagesAddingApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def patch(self, request):
        languages_from_body = set(request.data.get('languages'))
        if languages_from_body:
            specialist = request.user
            current_specialist_languages = specialist.languages.all()
            new_languages = [Language.objects.filter(name__iexact=lang).first()
                             for lang in languages_from_body]
            languages_for_adding = [language for language in filter(
                lambda lang: lang and lang not in current_specialist_languages,
                new_languages)]
            specialist.languages.add(*languages_for_adding)
        return Response(status=HTTP_200_OK)


class SpecialistLanguagesDeletionApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def patch(self, request):
        languages_from_body = set(request.data.get('languages'))
        if languages_from_body:
            specialist = request.user
            current_specialist_languages = specialist.languages.all()
            supposed_languages = [Language.objects.filter(name__iexact=lang).first()
                                  for lang in languages_from_body]
            languages_for_deletion = [language for language in
                                      filter(lambda lang: lang in current_specialist_languages,
                                             supposed_languages)]
            specialist.languages.remove(*languages_for_deletion)
        return Response(status=HTTP_200_OK)


class SpecialistTechnologiesAddingApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def patch(self, request):
        technologies_from_body = set(request.data.get('technologies'))
        if technologies_from_body:
            specialist = request.user
            current_specialist_technologies = specialist.technologies.all()
            new_technologies = [Technology.objects.filter(name__iexact=tech).first()
                                for tech in technologies_from_body]
            technologies_for_adding = [technology for technology in filter(
                lambda tech: tech and tech not in current_specialist_technologies,
                new_technologies)]
            specialist.technologies.add(*technologies_for_adding)
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class SpecialistTechnologiesDeletionApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def patch(self, request):
        technologies_from_body = request.data.get('technologies')
        if technologies_from_body:
            supposed_technologies = [Technology.objects.filter(name__iexact=lang).first()
                                     for lang in technologies_from_body]
            specialist = request.user
            exists_technologies = specialist.technologies.all()
            technologies_for_deletion = [technology for technology in
                                         filter(lambda tech: tech in exists_technologies,
                                                supposed_technologies)]
            specialist.technologies.remove(*technologies_for_deletion)
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class SpecialistDeletionApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self, request):
        specialist = request.user
        specialist.delete()
        return Response(status=HTTP_200_OK)