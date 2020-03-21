from distutils.core import setup
setup(
  name = 'hubdbapi',
  packages = ['hubdbapi'],
  version = '0.1',
  license='agpl-3.0',
  description = 'Python utilities for integrating with the HubDB API.',
  author = 'Mark Hansen',
  author_email = 'mark@rarekarma.com',
  url = 'https://github.com/khookguy/hubdbapi',
  download_url = 'https://github.com/khookguy/hubdbapi/archive/v_0.2.tar.gz',
  keywords = ['HubSpot', 'HubDB', 'API'],
  install_requires=[
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: GNU Affero General Public License v3',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)