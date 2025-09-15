from setuptools import setup, find_packages
from pathlib import Path

readme = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name='TkToolTip',
    version='1.12',
    author='Nenotriple',
    url='https://github.com/Nenotriple/TkToolTip',
    description='Add customizable tooltips to any Tkinter widget.',
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.10",
)
