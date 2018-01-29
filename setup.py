from setuptools import find_packages, setup


setup(
    name='pyserializer',
    version='0.9.1',
    description='Simple python serialization library.',
    author='LocalMed',
    author_email='ecordell@localmed.com, pete@localmed.com, joeljames1985@gmail.com',  # NOQA
    url='',
    license='MIT',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    install_requires=[
        'six==1.10.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
