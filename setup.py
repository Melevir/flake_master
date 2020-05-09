from typing import Optional

from setuptools import setup, find_packages


package_name = 'flake_master'


def get_version() -> Optional[str]:
    with open(f'{package_name}/__init__.py', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('__version__'):
            return line.split('=')[-1].strip().strip("'")


def get_long_description() -> str:
    with open('README.md', encoding='utf8') as f:
        return f.read()


setup(
    name=package_name,
    description='flake_master is a manager for flake8 plugins and configuration.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords='flake8 plugins',
    version=get_version(),
    author='Ilya Lebedev',
    author_email='melevir@gmail.com',
    install_requires=[
        'setuptools',
        'click>=7.1.2',
        'requirements-parser>=0.2.0',
        'requests>=2.23.0',
        'typing-extensions>=3.7.4.2',
    ],
    entry_points={
        'console_scripts': [
            'flake_master = flake_master.run:main',
        ],
    },
    url='https://github.com/Melevir/flake_master',
    license='MIT',
    py_modules=[package_name],
    zip_safe=False,
)
