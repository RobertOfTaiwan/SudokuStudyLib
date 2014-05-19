import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()

requires = []

setup(name='SudokuStudyLib',
      version='1.0.6',
      description='Sudoku Solving Library',
      long_description=README + '\n' + CHANGES,
      classifiers=[
          "Operating System :: OS Independent",
          "Environment :: Console",
          "Programming Language :: Python :: 3",
          "Topic :: Games/Entertainment :: Puzzle Games",
          "Topic :: Education",
          "Topic :: Scientific/Engineering :: Mathematics",
          "Intended Audience :: Developers",
          "Intended Audience :: Education",
          "Intended Audience :: End Users/Desktop",
          "Natural Language :: English",
          "Natural Language :: Chinese (Traditional)",
      ],
      author='Robert J. Hwang',
      author_email='RobertOfTaiwan@gmail.com',
      keywords='sudoku, python, studying',
      packages=['sudoku', 'matrix'],
      url = "https://github.com/RobertOfTaiwan/SudokuStudyLib",
      license='MIT',
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
)

