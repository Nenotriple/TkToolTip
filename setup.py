from setuptools import setup, find_packages

setup(
    name='TkToolTip',
    version='1.10',
    packages=find_packages(),
    install_requires=[],
    author='Nenotriple',
    author_email='...',
    description='Add customizable tooltips to any Tkinter widget.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Nenotriple/TkToolTip',
    python_requires='>=3.10',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
