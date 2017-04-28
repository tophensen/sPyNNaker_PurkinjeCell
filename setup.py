from setuptools import setup

setup(
    name="sPyNNaker7NewModelTemplate",
    version="1.0.0",
    packages=['python_models7',],
    package_data={'python_models7.model_binaries': ['*.aplx']},
    install_requires=['SpyNNaker >= 3.0.0, < 4.0.0']
)
