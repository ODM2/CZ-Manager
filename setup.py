import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.verbose = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


def extract_version(module='odm2djangoadmin'):
    version = None
    fdir = os.path.dirname(__file__)
    fnme = os.path.join(fdir, module, '__init__.py')
    with open(fnme) as fd:
        for line in fd:
            if (line.startswith('__version__')):
                _, version = line.split('=')
                # Remove quotation characters.
                version = version.strip()[1:-1]
                break
    return version

rootpath = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return open(os.path.join(rootpath, *parts), 'r').read()


long_description = '{}'.format(read('README.rst'))
LICENSE = read('LICENSE.txt')

with open('requirements.txt') as f:
    require = f.readlines()
install_requires = [r.strip() for r in require]

setup(name='odm2djangoadmin',
      version=extract_version(),
      license=LICENSE,
      long_description=long_description,
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Education',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Education',
                   ],
      description='Django admin app for Observation Data Model 2 (ODM2)',
      url='https://github.com/miguelcleon/odm2djangoadmin',
      platforms='any',
      keywords=['ODM2', 'Django'],
      install_requires=install_requires,
      packages=['odm2djangoadmin',
                'odm2djangoadmin/templatesAndSettings',
                'odm2djangoadmin/ODM2CZOData',
                'odm2djangoadmin/ODM2CZOData/migrations',
                'odm2djangoadmin/ODM2CZOData/templatetags'
                ],
      tests_require=['pytest'],
      cmdclass=dict(test=PyTest),
      author=['Miguel Leon'],
      author_email='leonmi@sas.upenn.edu',
      )
