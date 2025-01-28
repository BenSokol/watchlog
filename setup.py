import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name='watchlog',
  version='1.0.1',
  author='Ben Sokol',
  author_email='ben@bensokol.com',
  maintainer='Ben Sokol',
  maintainer_email='ben@bensokol.com',
  description='Watch logfile',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://git.bensokol.com/watchlog',
  download_url='https://git.bensokol.com/watchlog',
  project_urls={
    "Bug Tracker": "https://git.bensokol.com/watchlog/issues"
  },
  entry_points={
    'console_scripts': [
      'watchlog = watchlog.watchlog:main',
    ],
  },
  license='MIT',
  packages=['watchlog'],
)
