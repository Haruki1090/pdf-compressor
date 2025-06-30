#!/usr/bin/env python3
"""
PDF Compressor Setup Script
"""

from setuptools import setup, find_packages
import os

# README.mdの内容を読み込み
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name='pdf-compressor',
    version='1.0.0',
    description='高品質PDF圧縮CLIツール',
    long_description=read_readme() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/pdf-compressor',
    py_modules=['pdf-compressor'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'pdf-compress=pdf-compressor:main',
            'pdfcompress=pdf-compressor:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Office/Business',
        'Topic :: Utilities',
    ],
    keywords='pdf compression ghostscript cli tool',
    install_requires=[],
    extras_require={
        'dev': [
            'pytest',
            'black',
            'flake8',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/pdf-compressor/issues',
        'Source': 'https://github.com/yourusername/pdf-compressor',
    },
)