"""setup.py"""

from setuptools import setup

setup(name='mercadolibre_wrapper',
      version='0.1',
      description='',
      url='#',
      author='',
      author_email='',
      license='MIT',
      packages=['mercadolibre'],
      package_data={'': ['localhost.crt', 'localhost.key']},
      include_package_data=True,
      install_requires=[
          'requests',
      ],
      zip_safe=False)
