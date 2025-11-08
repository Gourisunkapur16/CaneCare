from setuptools import setup, find_packages

setup(
    name="cane-sight-ai",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'Flask>=2.3.3',
        'opencv-python>=4.8.1.78',
        'pytesseract>=0.3.10',
        'Pillow>=10.0.1',
    ],
)