from setuptools import setup, find_packages

setup(
    name='dates',
    version='0.0.1',
    author='Christophe-Marie Duquesne',
    author_email='chm.duquesne@gmail.com',
    packages=find_packages(),
    url='https://github.com/chmduquesne/dates',
    license=open('COPYING').read(),
    description='A small tool based on python-dateutil that just prints dates',
    long_description=open('README').read(),
    install_requires = ['python-dateutil'],
    entry_points=("""
    [console_scripts]
    dates = dates.dates:main
    """)
)

