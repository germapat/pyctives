import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyctivex',
    version='2.3.1',
    author='Habib E. Manzur',
    author_email='habibmanzur@outlook.com',
    description='Directorio activo para Emtelco',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/Emtelco_TIC/pyctivex',
    packages=setuptools.find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=['requests'],
    python_requires=">=3.0.*",
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ]

)
