from django.db import models

from core.models.choices import ProjectType


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    github_name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=False, blank=True, default='')
    version = models.CharField(max_length=20, null=False, blank=True, default='0.1')
    type = models.CharField(max_length=50, choices=ProjectType.choices)
    is_private = models.BooleanField(null=False, blank=True, default=False)
    start_date = models.DateField(auto_now=True)
    rating = models.BigIntegerField(null=False, blank=True, default=0)
    github = models.URLField(null=False, blank=True, default='')
    languages = models.ManyToManyField('core.Language', through='ProjectLanguage')
    technologies = models.ManyToManyField('core.Technology', through='ProjectTechnology')
    team = models.ManyToManyField('core.Specialist', through='ProjectTeam')
    owner = models.ForeignKey('core.Specialist', on_delete=models.CASCADE, related_name='owner')

    def __str__(self):
        return self.name


class ProjectLanguage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    language = models.ForeignKey('core.Language', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'language'],
                name='project__language__constraint',
            )
        ]


class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    technology = models.ForeignKey('core.Technology', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'technology'],
                name='project__technology__constraint',
            )
        ]


class ProjectTeam(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    specialist = models.OneToOneField('core.Specialist', on_delete=models.CASCADE)
