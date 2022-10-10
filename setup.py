import os
import re

from setuptools import setup, find_namespace_packages

# read requirements/dependencies
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# read description/README.md
with open("README.md", 'r') as fh:
    long_description = fh.read()


def get_h2_jars():
    jar_re = re.compile(r'h2-(?P<version>\d\.\d\.\d{3}).jar')
    jars = []
    for jar in os.listdir('pyelis/db/jar'):
        matcher = jar_re.match(jar)
        if matcher:
            jars.append(matcher.group('version'))

    print(f'Found {len(jars)} JAR files: {jars}')

    return jars


setup(name='pyelis-db',
      version='0.0.1.dev0',
      packages=find_namespace_packages(where='pyelis'),
      package_dir={"": "pyelis"},
      package_data={
          '': ['test_data/*'],
          'pyelis-db': [
              'pyelis/db/jar/h2-{}.jar'.format(version) for version in get_h2_jars()]
      },
      install_requires=requirements,

      long_description=long_description,
      long_description_content_type='text/markdown',

      author='Daniel Danis',
      author_email='daniel.gordon.danis@protonmail.com',
      url='https://github.com/ielis/pyelis-db',
      description='A bridge between Python and H2 database.',
      license='GPLv3',
      keywords='python, utilities, database, SQL, H2',
      zip_safe=False
      )
