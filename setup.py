from setuptools import setup, find_packages

version = '0.1'

setup(name='TracCommandHook',
      version=version,
      description="Trac plugin to execute a command after ticket change",
      long_description=open("README.rst").read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='trac plugin notify execute command ticket change',
      author='Laurent Lasudry',
      author_email='laurent.lasudry@affinitic.be',
      url='http://www.affinitic.be',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={
        'trac.plugins': [
            'TracCommandHook = traccommandhook',
        ],
      },
      )
