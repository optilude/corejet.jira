from setuptools import setup, find_packages

version = '1.0a1'

requires = [
    'setuptools',
    'suds',
    'corejet.core',
]

setup(name='corejet.jira',
      version=version,
      description="JIRA data source for corejet.testrunner",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='corejet JIRA',
      author='Martin Aspeli',
      author_email='optilude@gmail.com',
      url='http://corejet.org',
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['corejet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""
      [corejet.repositorysource]
      jira = corejet.jira.source:jiraSource
      """,
      )
