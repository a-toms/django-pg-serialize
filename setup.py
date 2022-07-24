from setuptools import setup

setup(
    name='django-pg-serializer',
    version='1.0.0',
    description='Uses postgres to directly convert your django model data to json',
    url='',
    author='a-toms',
    author_email='bright.joy5042@fastmail.com',
    license='MIT',
    packages=['django-pg-serializer'],
    install_requires=[
        'mpi4py>=2.0',
        'numpy',
    ],

    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
)
