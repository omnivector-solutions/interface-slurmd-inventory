from setuptools import find_packages, setup


setup(
    name='slurmd-inventory',
    packages=find_packages(include=['slurmd_inventory']),
    version='0.0.1',
    license='MIT',
    long_description=open('README.md', 'r').read(),
    url='https://github.com/omnivector-solutions/interface-slurmd-inventory',
    install_requires=[],
    python_requires='>=3.6',
)
