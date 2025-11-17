import distutils.cmd
import os
import subprocess

from setuptools import find_packages, setup


class BaseCommand(distutils.cmd.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


def create_command(text, commands):
    """Creates a custom setup.py command."""

    class CustomCommand(BaseCommand):
        description = text

        def run(self):
            for cmd in commands:
                subprocess.check_call(cmd)

    return CustomCommand


with open(
    os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
) as readme:
    README = readme.read()


setup(
    name="py-phone-number-fmt",
    version="2.0.2",
    packages=find_packages(),
    include_package_data=True,
    license="MIT License",
    description="Sanitize, validate and format phone numbers into E.164 valid phone numbers.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SectorLabs/py-phone-number-fmt",
    author="Sector Labs",
    author_email="open-source@sectorlabs.ro",
    keywords=["phone number", "phone", "formatting", "validation"],
    install_requires=["phonenumbers>=8.13.33,<=9.0.18"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    cmdclass={
        "lint": create_command(
            "Lints the code",
            [
                ["flake8", "setup.py", "phonenumberfmt", "tests"],
                ["pycodestyle", "setup.py", "phonenumberfmt", "tests"],
            ],
        ),
        "lint_fix": create_command(
            "Lints the code",
            [
                [
                    "autoflake",
                    "--remove-all-unused-imports",
                    "-i",
                    "-r",
                    "setup.py",
                    "phonenumberfmt",
                    "tests",
                ],
                ["autopep8", "-i", "-r", "setup.py", "phonenumberfmt", "tests"],
            ],
        ),
        "format": create_command(
            "Formats the code",
            [["black", "setup.py", "phonenumberfmt", "tests"]],
        ),
        "format_verify": create_command(
            "Checks if the code is auto-formatted",
            [["black", "--check", "setup.py", "phonenumberfmt", "tests"]],
        ),
        "format_docstrings": create_command(
            "Auto-formats doc strings", [["docformatter", "-r", "-i", "."]]
        ),
        "format_docstrings_verify": create_command(
            "Verifies that doc strings are properly formatted",
            [["docformatter", "-r", "-c", "."]],
        ),
        "sort_imports": create_command(
            "Automatically sorts imports",
            [
                ["isort", "setup.py"],
                ["isort", "-rc", "phonenumberfmt"],
                ["isort", "-rc", "tests"],
            ],
        ),
        "sort_imports_verify": create_command(
            "Verifies all imports are properly sorted.",
            [
                ["isort", "-c", "setup.py"],
                ["isort", "-c", "-rc", "phonenumberfmt"],
                ["isort", "-c", "-rc", "tests"],
            ],
        ),
        "fix": create_command(
            "Automatically format code and fix linting errors",
            [
                ["python", "setup.py", "format"],
                ["python", "setup.py", "format_docstrings"],
                ["python", "setup.py", "sort_imports"],
                ["python", "setup.py", "lint_fix"],
            ],
        ),
        "verify": create_command(
            "Verifies whether the code is auto-formatted and has no linting errors",
            [
                [
                    ["python", "setup.py", "format_verify"],
                    ["python", "setup.py", "format_docstrings_verify"],
                    ["python", "setup.py", "sort_imports_verify"],
                    ["python", "setup.py", "lint"],
                ]
            ],
        ),
    },
)
