from core.models.choices import ProjectType


def fill_languages(apps, schema_editor):
    Language = apps.get_model('core', 'Language')
    languages = (
        'Assembler',
        'APL',
        'C',
        'C++',
        'C#',
        'Clojure',
        'Crystal',
        'COBOL',
        'Delphi',
        'Dart',
        'Elixir',
        'Erlang',
        'F#',
        'Fortran',
        'Go',
        'Groovy',
        'Haskell',
        'Java',
        'JavaScript',
        'Julia',
        'Kotlin',
        'Lisp',
        'Lua',
        'Matlab',
        'Node.js',
        'Objective-C',
        'Python',
        'Perl',
        'PHP',
        'PowerShell',
        'R',
        'Rust',
        'Ruby',
        'Swift',
        'Scala',
        'Shell',
        'TypeScript',
        'Visual Basic',
    )

    Language.objects.bulk_create([Language(name=language) for language in languages])


def fill_technologies(apps, schema_editor):
    Technology = apps.get_model('core', 'Technology')
    technologies = (
        {'name': 'React', 'type': ProjectType.LIBRARY},

        {'name': 'Gin', 'type': ProjectType.FRAMEWORK},
        {'name': 'Django', 'type': ProjectType.FRAMEWORK},
        {'name': 'FastApi', 'type': ProjectType.FRAMEWORK},
        {'name': 'Flask', 'type': ProjectType.FRAMEWORK},
        {'name': 'Angular', 'type': ProjectType.FRAMEWORK},
        {'name': 'Vue', 'type': ProjectType.FRAMEWORK},

        {'name': 'MySQL', 'type': ProjectType.DATABASE},
        {'name': 'MongoDB', 'type': ProjectType.DATABASE},
        {'name': 'Postgres', 'type': ProjectType.DATABASE},
        {'name': 'Redis', 'type': ProjectType.DATABASE},
        {'name': 'Sqlite', 'type': ProjectType.DATABASE},
    )

    Technology.objects.bulk_create([Technology(**tech) for tech in technologies])
