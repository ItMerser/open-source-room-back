from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework.authtoken.models import Token

from core.models.choices import Direction


class SpecialistManager(BaseUserManager):
    def create_user(self, nickname: str, password: str, **extra_fields):
        specialist = self.model(nickname=nickname, **extra_fields)
        specialist.set_password(password)
        specialist.save()

        Token.objects.create(user=specialist)
        return specialist

    def create_superuser(self, nickname: str, password: str, **extra_fields):
        extra_fields['is_superuser'] = True
        return self.create_user(nickname, password, **extra_fields)


class Specialist(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(max_length=30, unique=True, db_index=True)
    github_nickname = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )
    direction = models.CharField(max_length=50, choices=Direction.choices)
    rating = models.PositiveIntegerField(null=False, blank=True, default=0)
    languages = models.ManyToManyField('core.Language', through='SpecialistLanguage')
    technologies = models.ManyToManyField('core.Technology', through='SpecialistTechnology')
    current_project = models.ForeignKey(
        'core.Project',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    projects = models.ManyToManyField(
        'core.Project',
        through='SpecialistProject',
        related_name='projects',
    )
    self_projects = models.ManyToManyField(
        'core.Project',
        through='SpecialistSelfProject',
        related_name='self_projects',
    )

    # additional information
    name = models.CharField(max_length=100, null=False, blank=True, default='')
    surname = models.CharField(max_length=255, null=False, blank=True, default='')
    born_date = models.DateField(null=True, blank=True, default=None)
    about = models.TextField(null=False, blank=True, default='')
    country = models.CharField(max_length=255, blank=True, default='')
    city = models.CharField(max_length=255, blank=True, default='')
    email = models.EmailField(null=False, blank=True, default='')
    github = models.URLField(null=False, blank=True, default='')

    # default fields
    last_login = None
    is_private = models.BooleanField(null=False, blank=True, default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = SpecialistManager()

    USERNAME_FIELD = 'nickname'

    def __str__(self):
        return self.nickname


class SpecialistProject(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    project = models.ForeignKey('core.Project', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['specialist', 'project'],
                name='specialist__project__constraint',
            )
        ]


class SpecialistSelfProject(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    self_project = models.ForeignKey('core.Project', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['specialist', 'self_project'],
                name='specialist__self_project__constraint',
            )
        ]


class SpecialistLanguage(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    language = models.ForeignKey('core.Language', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['specialist', 'language'],
                name='specialist__language__constraint'),
        ]


class SpecialistTechnology(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    technology = models.ForeignKey('core.Technology', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['specialist', 'technology'],
                name='specialist__technology__constraint'),
        ]
