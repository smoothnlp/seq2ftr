import setuptools

setuptools.setup(
    name="ager",
    version="0.1",
    author="Ruinan(Victor) Zhang",
    author_email="ruinan.zhang@icloud.com",
    description="A Nice and Convenient Feature Engineering Tool on Sequential Data",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/zhangruinan/Ager",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        "sklearn"
        "logging"
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],