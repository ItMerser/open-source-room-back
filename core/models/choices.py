from django.db import models


# For core.Specialist
class Direction(models.TextChoices):
    BACKEND = ('BACKEND', 'BACKEND')
    FRONTEND = ('FRONTEND', 'FRONTEND')
    DEVOPS = ('DEVOPS', 'DEVOPS')
    GAME_DEV = ('GAME DEV', 'GAME DEV')
    MOBILE = ('MOBILE', 'MOBILE')
    DESKTOP = ('DESKTOP', 'DESKTOP')
    EMBEDDED = ('EMBEDDED', 'EMBEDDED')
    DATA_SCIENTIST = ('DATA SCIENTIST', 'DATA SCIENTIST')
    DATA_ANALYST = ('DATA ANALYST', 'DATA ANALYST')
    DATA_ENGINEER = ('DATA ENGINEER', 'DATA ENGINEER')
    QA = ('QA', 'QA')
    CUSTOMER = ('CUSTOMER', 'CUSTOMER')


# For core.Project
class ProjectType(models.TextChoices):
    LIBRARY = ('LIBRARY', 'LIBRARY')
    FRAMEWORK = ('FRAMEWORK', 'FRAMEWORK')
    SPA = ('SPA', 'SPA')
    WEB_APPLICATION = ('WEB APPLICATION', 'WEB APPLICATION')
    SERVICE = ('SERVICE', 'SERVICE')
    DRIVER = ('DRIVER', 'DRIVER')
    MICROCONTROLLER = ('MICROCONTROLLER', 'MICROCONTROLLER')
    GAME = ('GAME', 'GAME')
    OS = ('OS', 'OS')
    DATABASE = ('DATABASE', 'DATABASE')
    DATABASE_MANAGEMENT_SYSTEM = ('DATABASE MANAGEMENT SYSTEM', 'DATABASE MANAGEMENT SYSTEM')
    COMPILER = ('COMPILER', 'COMPILER')
    INTERPRETER = ('INTERPRETER', 'INTERPRETER')
    PROGRAM_LANGUAGE = ('PROGRAM LANGUAGE', 'PROGRAM LANGUAGE')
    ARCHIVER = ('ARCHIVER', 'ARCHIVER')
    ANTIVIRUS = ('ANTIVIRUS', 'ANTIVIRUS')
    FIREWALL = ('FIREWALL', 'FIREWALL')
    REDACTOR = ('REDACTOR', 'REDACTOR')
    BROWSER = ('BROWSER', 'BROWSER')
    FILE_MANAGER = ('FILE MANAGER', 'FILE MANAGER')


# For core.Offer
class OfferType(models.TextChoices):
    JOIN_TO_TEAM = ('JOIN_TO_TEAM', 'JOIN_TO_TEAM')
    ADD_TO_TEAM = ('ADD_TO_TEAM', 'ADD_TO_TEAM')
    GIVE_OWNERSHIP = ('GIVE_OWNERSHIP', 'GIVE_OWNERSHIP')
    GET_OWNERSHIP = ('GET_OWNERSHIP', 'GET_OWNERSHIP')
