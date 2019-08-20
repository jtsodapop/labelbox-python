import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="labelbox",
    version="0.0.1",
    author="Kyle Owens",
    author_email="kyle@labelbox.com",
    description="Labelbox pip Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/labelbox/labelbox-pip",
    packages=setuptools.find_packages(),
    classifiers=[],
)
