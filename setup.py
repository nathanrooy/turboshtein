import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    author='Nathan A. Rooy',
    author_email='nathanrooy@gmail.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: C'
    ],
    description='Levenshtein edit distance computed quickly',
    ext_modules=[
        setuptools.Extension('turboshtein', sources=['turboshtein.c'])
    ],
    keywords=['levenshtein distance'],
    license='MIT License',
    long_description=long_description,
    long_description_content_type="text/markdown",
    name='turboshtein',
    python_requires='>=3.4',
    url='https://githubcom/nathanrooy/turboshtein',
    version='0.0.4'
)
