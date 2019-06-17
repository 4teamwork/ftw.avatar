import os
from setuptools import setup, find_packages


version = '2.1.0'


tests_require = [
    'ftw.builder',
    'ftw.testbrowser',
    'plone.app.testing',
    'transaction',
    'unittest2',
    'zope.configuration',
    ]


setup(name='ftw.avatar',
      version=version,
      description='Generates a personal default avatar for new Plone users',

      long_description=open('README.rst').read() + '\n' + \
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw avatar personal user portrait plone',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.avatar',

      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'AccessControl',
        'Pillow',
        'Products.CMFCore',
        'Products.PlonePAS',
        'Zope2',
        'plone.scale',
        'setuptools',
        'zope.annotation',
        'zope.component',
        'zope.interface',
        'Plone',
        ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
