#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [x for x in fh.read().splitlines() if x]

setup(name='imagestack_svg',
      packages=['imagestack_svg'],
      version='1.1.1',
      description='Create Images by Stacking them',
      author='skillor',
      author_email='skillor@gmx.net',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      url='https://github.com/skillor/imagestack-svg-python',
      keywords=['image', 'imagestack', 'imagestack-svg', 'imagestack_svg', 'svg'],
      classifiers=['Programming Language :: Python :: 3 :: Only',
                   'Programming Language :: Python :: 3.9',
                   'Topic :: Multimedia :: Graphics'],
      setup_requires=["wheel"],
      install_requires=requirements,
      python_requires='>=3',
      )
