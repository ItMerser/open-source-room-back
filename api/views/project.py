from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView

from api.permissions import IsProjectOwner
from api.serializers.project import (
    ProjectSerializer,
    ProjectCreationSerializer,
    ProjectUpdatingSerializer,
)
from core.models import Project, Specialist, Language, Technology


class ProjectsListApiView(APIView):
    def get(self, request):
        projects = Project.objects.filter(is_private=False) \
            .prefetch_related('languages', 'technologies', 'team')
        serializer = ProjectSerializer(projects, many=True)
        return Response(status=HTTP_200_OK, data=serializer.data)


class ProjectRetrieveApiView(APIView):
    def get(self, request, project_id: int):
        try:
            project = Project.objects.prefetch_related('languages', 'technologies', 'team') \
                .get(pk=project_id)
        except Project.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project)
        return Response(status=HTTP_200_OK, data=serializer.data)


class ProjectCreationApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = ProjectCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        specialist = Specialist.objects.get(nickname=request.user.nickname)
        serializer.validated_data['owner'] = specialist
        project = serializer.save()

        specialist.self_projects.add(project)

        serialized_project = ProjectSerializer(project)
        return Response(status=HTTP_201_CREATED, data=serialized_project.data)


class ProjectUpdatingApiView(APIView):
    permission_classes = [IsAuthenticated, IsProjectOwner]
    authentication_classes = [TokenAuthentication]

    def patch(self, request, project_id: int):
        project = Project.objects.get(pk=project_id)
        serializer = ProjectUpdatingSerializer(instance=project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_200_OK)


class ProjectLanguagesAddingApiView(APIView):
    permission_classes = [IsAuthenticated, IsProjectOwner]
    authentication_classes = [TokenAuthentication]

    def patch(self, request, project_id: int):
        languages_from_body = request.data.get('languages')
        if languages_from_body:
            new_languages = [Language.objects.filter(name__iexact=lang).first()
                             for lang in languages_from_body]
            project = Project.objects.get(pk=project_id)
            exists_languages = project.languages.all()
            languages_for_adding = [language for language in filter(
                lambda lang: lang and lang not in exists_languages,
                new_languages)]
            project.languages.add(*languages_for_adding)
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class ProjectLanguagesDeletionApiView(APIView):
    permission_classes = [IsAuthenticated, IsProjectOwner]
    authentication_classes = [TokenAuthentication]

    def patch(self, request, project_id: int):
        languages_from_body = request.data.get('languages')
        if languages_from_body:
            supposed_languages = [Language.objects.filter(name__iexact=lang).first()
                                  for lang in languages_from_body]
            project = Project.objects.get(pk=project_id)
            exists_languages = project.languages.all()
            languages_for_deletion = [language for language in
                                      filter(lambda lang: lang in exists_languages,
                                             supposed_languages)]
            project.languages.remove(*languages_for_deletion)
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class ProjectTechnologiesAddingApiView(APIView):
    permission_classes = [IsAuthenticated, IsProjectOwner]
    authentication_classes = [TokenAuthentication]

    def patch(self, request, project_id: int):
        technologies_from_body = request.data.get('technologies')
        if technologies_from_body:
            new_technologies = [Technology.objects.filter(name__iexact=lang).first()
                                for lang in technologies_from_body]
            project = Project.objects.get(pk=project_id)
            exists_technologies = project.technologies.all()
            technologies_for_adding = [technology for technology in
                                       filter(lambda tech: tech and tech not in exists_technologies,
                                              new_technologies)]
            project.technologies.add(*technologies_for_adding)
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class ProjectTechnologiesDeletionApiView(APIView):
    permission_classes = [IsAuthenticated, IsProjectOwner]
    authentication_classes = [TokenAuthentication]

    def patch(self, request, project_id: int):
        technologies_from_body = request.data.get('technologies')
        if technologies_from_body:
            supposed_technologies = [Technology.objects.filter(name__iexact=lang).first()
                                     for lang in technologies_from_body]
            project = Project.objects.get(pk=project_id)
            exists_technologies = project.technologies.all()
            technologies_for_deletion = [technology for technology in
                                         filter(lambda tech: tech in exists_technologies,
                                                supposed_technologies)]
            project.technologies.remove(*technologies_for_deletion)
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class ProjectDeletionApiView(APIView):
    permission_classes = [IsAuthenticated, IsProjectOwner]
    authentication_classes = [TokenAuthentication]

    def delete(self, request, project_id: int):
        try:
            project_for_delete = Project.objects.get(pk=project_id)
            response_data = {'deleted_project_pk': project_for_delete.pk}
            project_for_delete.delete()
            return Response(status=HTTP_200_OK, data=response_data)
        except Project.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
