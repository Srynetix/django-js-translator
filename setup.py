"""Django JS Translator."""

from setuptools import setup
from django_js_translator.version import __version__

setup(
    name='django-js-translator',
    version=__version__,
    description='Translate JS strings for Django',
    url='',
    author='SharingCloud',
    author_email='',
    license='MIT',
    packages=['django_js_translator'],
    install_requires=[
        'colorama',
        'PyYAML'
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'django-js-translator = django_js_translator.shell:entry_point',
        ]
    },
)
