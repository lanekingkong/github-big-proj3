from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="bioomics-bridge",
    version="1.0.0",
    author="BioOmicsBridge Team",
    author_email="team@bioomicsbridge.org",
    description="AI-Powered Multi-Omics Data Integration and Drug Target Discovery Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/BioOmicsBridge",
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0",
            "isort>=5.12",
            "mypy>=1.5",
            "pre-commit>=3.4",
            "mkdocs>=1.5",
            "mkdocs-material>=9.0",
        ],
        "gpu": [
            "torch>=2.0",
            "cupy-cuda11x>=12.0",
        ],
        "full": [
            "anndata>=0.10",
            "scanpy>=1.9",
            "scvi-tools>=0.20",
            "networkx>=3.1",
            "scikit-learn>=1.3",
        ],
    },
    entry_points={
        "console_scripts": [
            "bioomics-bridge=bioomics_bridge.cli:main",
        ],
    },
)