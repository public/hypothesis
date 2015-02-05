from distutils.core import setup
from setuptools.command.test import test as TestCommand
from setuptools import find_packages
import sys


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='hypothesis-pytest',
    version='0.1.0',
    author='David R. MacIver',
    author_email='david@drmaciver.com',
    packages=find_packages("src"),
    package_dir={"": "src"},
    url='https://github.com/DRMacIver/hypothesis',
    license='MPL v2',
    description='Pytest plugin for better integration with hypothesis',
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        'hypothesis.extra': 'hypothesispytest = hypothesispytest:load',
         'pytest11': ['hypothesispytest = hypothesispytest'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Testing",
    ],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)
