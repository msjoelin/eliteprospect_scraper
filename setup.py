from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='eliteprospect_scraper',
    version='0.6',
    description='Functions to scrape ice hockey data from eliteprospects',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Marcus Sjölin',
    author_email='marcussjolin89@gmail.com',
    keywords=['ice hockey', 'scraping', 'sport analytics', 'datetime', 'time', 'requests'],
    url='https://github.com/msjoelin/eliteprospect_scraper',
    download_url='https://pypi.org/project/eliteprospect_scraper/'
)

install_requires = [
    'numpy',
    'pandas',
    'bs4',
    'datetime'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)