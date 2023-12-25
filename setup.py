from setuptools import find_packages, setup

setup(
    name="travel_time_comparison",
    version="0.0.1",
    description="Analysis of travel times of different modes of transportation across europe.",
    author="Tibor Čuš",
    author_email="cus.tibor@outlook.com",
    license="MIT",
    install_requires=[
        "numpy==1.23.3",
        "pandas==1.5.0",
        "scikit-learn==1.1.2",
        "matplotlib==3.8.2",
        "seaborn==0.13.0",
        "countryinfo==0.1.2",
        "networkx==3.2.1",
        "tqdm==4.66.1",
        "requests==2.31.0"
    ],
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    zip_safe=False,
)
