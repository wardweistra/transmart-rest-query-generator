from setuptools import setup, find_packages

NAME = 'TranSMART REST Query Generator'
VERSION = '0.1'
mainscript = 'runserver.py'

setup(
    name=NAME,
    version=VERSION,
    description='TranSMART REST Query Generator',
    url='https://github.com/wardweistra/transmart-rest-query-generator',
    author='Ward Weistra',
    author_email='ward@thehyve.nl',
    license='GNU General Public License V3',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask'],
    scripts=[mainscript],
)
