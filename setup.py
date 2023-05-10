from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='virshstat',
    version='1.0.0',
    package_dir={"": "src/virshstat"},
    py_modules=['virshstat'],
    include_package_data=True,
    install_requires=[''],
    long_description=readme()
)
