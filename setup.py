"""
Setup script for EncryptDecrypt package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="encryptdecrypt",
    version="2.0.0",
    author="KleaSCM",
    author_email="KleaSCM@gmail.com",
    description="Advanced File Encryption System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KleaSCM/encryptdecrypt",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security :: Cryptography",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "encryptdecrypt=encryptdecrypt.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "encryptdecrypt": ["*.yaml", "*.txt"],
    },
    keywords="encryption, cryptography, security, file, gui, cli",
    project_urls={
        "Bug Reports": "https://github.com/KleaSCM/encryptdecrypt/issues",
        "Source": "https://github.com/KleaSCM/encryptdecrypt",
        "Documentation": "https://github.com/KleaSCM/encryptdecrypt#readme",
    },
) 