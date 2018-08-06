
import setuptools

with open('README.md', 'r') as f:

    long_description = f.read()

setuptools.setup(
    name='mbta',
    version='0.0.3',
    author='Jared Stufft',
    author_email='jared@stufft.us',
    description='A simple, high-level Python wrapper for the MBTA API',
    long_description=long_description,
    url='https://github.com/JaredStufft/mbta',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Development Status :: 3 - Alpha'
    )
)