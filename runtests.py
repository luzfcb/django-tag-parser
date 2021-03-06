#!/usr/bin/env python
import sys
import django
from django.conf import settings, global_settings as default_settings
from django.core.management import execute_from_command_line
from os import path


# Give feedback on used versions
sys.stderr.write('Using Python version {0} from {1}\n'.format(sys.version[:5], sys.executable))
sys.stderr.write('Using Django version {0} from {1}\n'.format(
    django.get_version(),
    path.dirname(path.abspath(django.__file__)))
)

if not settings.configured:
    module_root = path.dirname(path.realpath(__file__))

    if django.VERSION >= (1, 8):
        template_settings = dict(
            TEMPLATES = [
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'OPTIONS': {
                        'loaders': (
                            'django.template.loaders.filesystem.Loader',
                            'django.template.loaders.app_directories.Loader',
                        ),
                        'context_processors': (
                            'django.template.context_processors.request',
                        ),
                    },
                },
            ]
        )

        if django.VERSION >= (1, 9):
            template_settings['TEMPLATES'][0]['OPTIONS'].update({
                'builtins': [
                    'tag_parser.tests.templatetags.tag_parser_test_tags',
                ],
            })
    else:
        template_settings = dict(
            TEMPLATE_LOADERS = (
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.filesystem.Loader',
            ),
            TEMPLATE_CONTEXT_PROCESSORS = [
                'django.core.context_processors.request',
            ],
        )

    settings.configure(
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        INSTALLED_APPS = (
            'tag_parser',
            'tag_parser.tests',
        ),
        MIDDLEWARE_CLASSES = default_settings.MIDDLEWARE_CLASSES,  # silencens Django 1.7 checks
        TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner' if django.VERSION < (1, 6) else 'django.test.runner.DiscoverRunner',
        **template_settings
    )

DEFAULT_TEST_APPS = [
    'tag_parser',
]


def runtests():
    other_args = list(filter(lambda arg: arg.startswith('-'), sys.argv[1:]))
    test_apps = list(filter(lambda arg: not arg.startswith('-'), sys.argv[1:])) or DEFAULT_TEST_APPS
    argv = sys.argv[:1] + ['test', '--traceback'] + other_args + test_apps
    execute_from_command_line(argv)

if __name__ == '__main__':
    runtests()
