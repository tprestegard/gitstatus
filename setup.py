import os
import re
from setuptools import setup, find_packages


def parse_version(path):
    """Extract the `__version__` string from the given file"""
    with open(path, 'r') as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Classifiers
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    ('License :: OSI Approved :: GNU General Public License v3 or later '
        '(GPLv3+)'),
    'Operating System :: POSIX',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Software Development :: Version Control :: Git',
]


###############################################################################
# Call setup() ################################################################
###############################################################################
setup(
    name="gitstatus",
    version=parse_version(os.path.join("gitstatus", "version.py")),
    author=("Tanner Prestegard"),
    author_email="tprestegard@gmail.com",
    description=("A Python package for checking the status of your local git "
                 "repositories"),
    license="GPL-3.0-or-later",
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    install_requires=("Click==7.0",),
    entry_points={
        "console_scripts": ("gitstatus=gitstatus.script:main",)
    },
)
