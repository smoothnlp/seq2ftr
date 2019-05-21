import setuptools

setuptools.setup(
    name="seq2ftr",
    version="0.1.5",
    author="Ruinan(Victor) Zhang， YinJun(YJ)",
    author_email="ruinan.zhang@icloud.com, yjun1989@gmail.com",
    description="A Nice and Convenient Feature Engineering Tool on Sequential Data",
    long_description='readme.rst',
    long_description_content_type="",
    url="https://github.com/smoothnlp/seq2ftr",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        "sklearn"
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ])