from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='vcsd',
    version='0.1',
    description='Package to encrypt short messages',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Topic :: Cryptography',
    ],
    author='Enrique Pedruelo',
    author_email="epedruelo5@gmail.com",
    packages=['vcsd'],  
    install_requires=[
        'qrcode',
    ],
    include_package_data=True,
    zip_safe=False
)