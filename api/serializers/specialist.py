from datetime import date

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import Specialist, Project
from core.models.choices import Direction

SpecialistModel = get_user_model()


class SpecialistProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'github_name', 'version', 'type', 'rating', 'github',)


class SpecialistSerializer(serializers.ModelSerializer):
    languages = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    technologies = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    current_project = SpecialistProjectSerializer(read_only=True)
    projects = SpecialistProjectSerializer(many=True, read_only=True)
    own_projects = SpecialistProjectSerializer(many=True, read_only=True)
    age = serializers.SerializerMethodField()

    class Meta:
        model = Specialist
        fields = ('id', 'nickname', 'github_nickname', 'direction', 'rating', 'languages',
                  'technologies', 'current_project', 'projects', 'own_projects', 'email', 'github',
                  'name', 'surname', 'age', 'country', 'city', 'about',)
        depth = 1

    def get_age(self, obj) -> int | None:
        if obj.born_date:
            return self._full_years(born_date=obj.born_date)
        return None

    def _full_years(self, born_date: date) -> int:
        current_date = date.today()
        if current_date.month < born_date.month:
            return current_date.year - born_date.year - 1
        elif current_date.month == born_date.month and current_date.day < born_date.day:
            return current_date.year - born_date.year - 1
        return current_date.year - born_date.year


class SpecialistCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialistModel
        fields = ('nickname', 'github_nickname', 'password', 'direction', 'email', 'github', 'name',
                  'surname', 'born_date', 'about', 'country', 'city',)

    def create(self, validated_data):
        specialist = SpecialistModel.objects.create_user(**validated_data)
        return specialist


class SpecialistAuthenticationSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(max_length=30)

    class Meta:
        model = Specialist
        fields = ('nickname', 'password',)

    def validate(self, attrs):
        try:
            specialist = Specialist.objects.get(nickname=attrs['nickname'])
            password = attrs['password']
            if specialist.check_password(password):
                return attrs
        except Specialist.DoesNotExist:
            raise serializers.ValidationError('Invalid authentication data')
        raise serializers.ValidationError('Invalid authentication data')


class SpecialistUpdatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = ('nickname', 'github_nickname', 'direction', 'email', 'github', 'name', 'surname',
                  'born_date', 'about', 'country', 'city',)

    def validate_direction(self, value):
        if type(value) is str and value.upper() in Direction.values:
            return value.upper()
        raise ValidationError('Invalid direction')
