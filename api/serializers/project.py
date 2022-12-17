from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import Project, Specialist
from core.models.choices import ProjectType


class ProjectSpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = ('id', 'nickname', 'github_nickname', 'direction', 'rating', 'github',)


class ProjectSerializer(serializers.ModelSerializer):
    languages = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    technologies = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    team = ProjectSpecialistSerializer(many=True, read_only=True)
    owner = ProjectSpecialistSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'github_name', 'description', 'version', 'type', 'start_date',
                  'rating', 'github', 'languages', 'technologies', 'team', 'owner',)
        depth = 1


class ProjectCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'github_name', 'description', 'version', 'type', 'is_private', 'github',)


class ProjectUpdatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'github_name', 'description', 'version', 'type', 'is_private', 'github',)

    def validate_type(self, value):
        if type(value) is str and value.upper() in ProjectType.values:
            return value.upper()
        raise ValidationError('Invalid project type')
