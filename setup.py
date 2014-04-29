import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = []

setup(name='SudokuStudyLib',
      version='0.5',
      description='Sudoku Solving Library',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Environment :: Console",
          "Programming Language :: Python",
          "Topic :: Games/Entertainment :: Puzzle Games",
          "Topic :: Education",
      ],
      author='Robert J. Hwang',
      author_email='RobertOfTaiwan@gmail.com',
      keywords='sudoku, python, studying',
      packages=['sudoku', 'matrix'],
      license='MIT',
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
)

