from setuptools import setup, find_packages

with open("README_unified.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements_unified.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="professional-document-suite",
    version="1.0.0",
    author="Professional Document Suite Team",
    author_email="",
    description="A comprehensive tool for PDF manipulation and image conversion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/professional-document-suite",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pdf-tools=unified_app.app:main",
        ],
    },
)