import setuptools
import os
rootdir = os.path.abspath(os.path.dirname(__file__))
long_description = open(os.path.join(rootdir, 'readme.rst')).read()

setuptools.setup(
    name="seq2ftr",
    version="0.1.7",
    author="Ruinan(Victor) Zhang， YinJun(YJ)",
    author_email="ruinan.zhang@icloud.com, yjun1989@gmail.com",
    description="A Nice and Convenient Feature Engineering Tool on Sequential Data",
    long_description=long_description,
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