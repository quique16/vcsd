from setuptools import setup, find_packages

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
    packages=find_packages(),
    install_requires=[
        'qrcode',
        'numpy',
        'Pillow',
        'opencv-python'
    ],
    python_requires='>=3.6',
    extras_require={
        'docs': ['numpydoc', 'sphinx!=1.3.1', 'sphinx_rtd_theme',
                 'matplotlib >= 2.0.0',
                 'sphinxcontrib-versioning >= 2.2.1',
                 'sphinx-gallery',
                 'presets'],
        'tests': ['matplotlib >= 2.1',
                  'pytest-mpl',
                  'pytest-cov',
                  'pytest',
                  'contextlib2',
                  'samplerate'],
        'display': ['matplotlib >= 1.5'],
    },
    include_package_data=True,
    zip_safe=False
)