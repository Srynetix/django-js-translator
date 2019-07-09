"""Django JS Translator."""

import distutils.cmd
import distutils.log
import subprocess
import sys
from typing import List, Tuple

from setuptools import setup

from django_js_translator.version import __version__


class LintCommand(distutils.cmd.Command):
    """Lint with flake8."""

    description = "run flake8 on source files"
    user_options = [("path", "p", "path")]

    def initialize_options(self):
        self.path = None

    def finalize_options(self):
        if self.path is None:
            self.path = "."

    def run(self):
        try:
            self.announce(f"linting files on path {self.path} ...")
            subprocess.check_call(["flake8", self.path])
        except subprocess.CalledProcessError:
            sys.exit(1)


class FormatCommand(distutils.cmd.Command):
    """Format with black."""

    description = "run black and isort on source files"
    user_options = [("path=", "p", "path")]

    def initialize_options(self):
        self.path = None

    def finalize_options(self):
        if self.path is None:
            self.path = "."

    def run(self):
        self.announce(f"formatting files on path {self.path} ...")

        try:
            self.announce("> isort ...")
            subprocess.check_call(["isort", "-rc", "--atomic", self.path])
        except subprocess.CalledProcessError:
            sys.exit(1)

        try:
            self.announce("> black ...")
            subprocess.check_call(["black", "--target-version", "py36", "-l", "120", self.path])
        except subprocess.CalledProcessError:
            sys.exit(1)


class FormatCheckCommand(distutils.cmd.Command):
    """Format check with black."""

    description = "run black check on source files"
    user_options = [("path=", "p", "path")]

    def initialize_options(self):
        self.path = None

    def finalize_options(self):
        if self.path is None:
            self.path = "."

    def run(self):
        try:
            self.announce(f"checking if files are formatted on path {self.path} ...")
            subprocess.check_call(["black", "--target-version", "py36", "-l", "120", "--check", self.path])
        except subprocess.CalledProcessError:
            sys.exit(1)


class TypeCheckCommand(distutils.cmd.Command):
    """Typecheck with mypy."""

    description = "run mypy on source files"
    user_options = [("path", "p", "path")]

    def initialize_options(self):
        self.path = None

    def finalize_options(self):
        if self.path is None:
            self.path = "."

    def run(self):
        try:
            self.announce(f"type checking in path {self.path} ...")
            subprocess.check_call(["mypy", self.path])
        except subprocess.CalledProcessError:
            sys.exit(1)


class CICommand(distutils.cmd.Command):
    """Run CI."""

    description = "run ci"
    user_options: List[Tuple] = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.announce(f"running CI ...")
        self.run_command("typecheck")
        self.run_command("fmtcheck")
        self.run_command("lint")


setup(
    name="django-js-translator",
    version=__version__,
    description="Translate JS strings for Django",
    url="",
    author="Denis BOURGE",
    author_email="",
    license="MIT",
    packages=["django_js_translator"],
    zip_safe=False,
    entry_points={"console_scripts": ["django-js-translator = django_js_translator.shell:entry_point"]},
    cmdclass={
        "lint": LintCommand,
        "fmt": FormatCommand,
        "fmtcheck": FormatCheckCommand,
        "typecheck": TypeCheckCommand,
        "ci": CICommand,
    },
)
