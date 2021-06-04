# This file was auto-generated by Shut. DO NOT EDIT
# For more information about Shut, check out https://pypi.org/project/shut/

from __future__ import print_function
import io
import os
import setuptools
import sys

def _tempcopy(src, dst):
  import atexit, shutil
  if not os.path.isfile(dst):
    if not os.path.isfile(src):
      print('warning: source file "{}" for destination "{}" does not exist'.format(src, dst))
      return
    shutil.copyfile(src, dst)
    atexit.register(lambda: os.remove(dst))


_tempcopy('../LICENSE.txt', 'LICENSE.txt')

readme_file = 'README.md'
if os.path.isfile(readme_file):
  with io.open(readme_file, encoding='utf8') as fp:
    long_description = fp.read()
else:
  print("warning: file \"{}\" does not exist.".format(readme_file), file=sys.stderr)
  long_description = None

requirements = [
  'dataclasses >=0.6.0,<1.0.0',
  'nr.optional >=0.1.0,<1.0.0',
  'nr.preconditions >=0.0.2,<1.0.0',
  'nr.pylang.utils >=0.1.1,<1.0.0',
  'nr.stream >=0.1.1,<1.0.0',
]

setuptools.setup(
  name = 'databind.core',
  version = '0.11.0',
  author = 'Niklas Rosenstein',
  author_email = 'rosensteinniklas@gmail.com',
  description = 'Databind is a library inspired by Jackson-databind to describe and bind data models for object-oriented programming.',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/NiklasRosenstein/python-databind',
  license = 'MIT',
  packages = setuptools.find_packages('src', ['test', 'test.*', 'tests', 'tests.*', 'docs', 'docs.*']),
  package_dir = {'': 'src'},
  include_package_data = True,
  install_requires = requirements,
  extras_require = {},
  tests_require = [],
  python_requires = '>=3.6.0,<4.0.0',
  data_files = [],
  entry_points = {},
  cmdclass = {},
  keywords = [],
  classifiers = [],
  zip_safe = False,
)
