import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='hasami',
    version='0.0.1',
    description='Sentence segmentation for japanese text',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mkartawijaya/hasami',
    author='Martin Kartawijaya',
    author_email='pypi@m.kartawijaya.dev',
    license='BSD-3-Clause',
    packages=setuptools.find_packages(include=['hasami']),
    keywords=['japanese', 'sentence', 'segmentation', 'nlp', 'sbd'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Topic :: Text Processing :: Linguistic',
        'Natural Language :: Japanese'
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['hasami=hasami.cli:main']
    }
)
