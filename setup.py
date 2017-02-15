#!/usr/bin/env python3


from setuptools import setup


setup(name='aft',
      version='0.2.0',
      description='',
      author='Steven J. Core',
      author_email='42Echo6Alpha@gmail.com',
      license='GPL3.0',
      packages=['aft'],
      zip_safe=False,
      include_package_data=True,
      install_requires=['pyyaml', 'urwid'],
      entry_points={
        'console_scripts': [
            'aft = aft.program:main'
         ]
      })
