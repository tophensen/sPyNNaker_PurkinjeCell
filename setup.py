from setuptools import setup

setup(
    name="sPyNNaker7NewModelTemplate",
    version="1!4.0.0a5",
    packages=['python_models7'],
    package_data={'python_models7.model_binaries': ['*.aplx']},
    install_requires=[
        'SpiNNUtilities >= 1!4.0.0a5, < 1!5.0.0',
        'SpiNNStorageHandlers >= 1!4.0.0a5, < 1!5.0.0',
        'SpiNNMachine >= 1!4.0.0a5, < 1!5.0.0',
        'SpiNNMan >= 1!4.0.0a5, < 1!5.0.0',
        'SpiNNaker_PACMAN >= 1!4.0.0a5, < 1!5.0.0',
        'SpiNNaker_DataSpecification >= 1!4.0.0a5, < 1!5.0.0',
        'spalloc >= 0.2.2, < 1.0.0',
        'SpiNNFrontEndCommon >= 1!4.0.0a5, < 1!5.0.0',
        'sPyNNaker >= 1!4.0.0a5, < 1!5.0.0',
        'SpyNNaker7 >= 1!4.0.0a5, < 1!5.0.0']
)
