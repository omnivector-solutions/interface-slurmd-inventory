from setuptools import find_packages, setup


setup(
    name='slurmd-peer',
    packages=find_packages(include=['slurmd_peer']),
    version='0.0.1',
    license='MIT',
    long_description=open('README.md', 'r').read(),
    url='https://github.com/omnivector-solutions/interface-slurmd-peer',
    install_requires=[],
    python_requires='>=3.6',
)
