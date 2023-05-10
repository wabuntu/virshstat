from setuptools import setup

setup(
    name='virshstat',
    version='1.0.0',
    package_dir={"": "src/virshstat"},
    py_modules=['virshstat'],
    include_package_data=True,
    install_requires=[''],
    long_description=readme
)
