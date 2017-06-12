from setuptools import setup

setup(
    name="sPyNNaker7NewModelTemplate",
    version="1!4.0.0a5",
    packages=['python_models7'],
    package_data={'python_models7.model_binaries': ['*.aplx']},
    install_requires=['SpyNNaker >= 1!4.0.0a5, < 1!5.0.0']
)
