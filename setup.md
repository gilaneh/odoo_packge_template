## prerequisites:
[Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
### setup a virtual environment:
`apt-get install python3-venv`

`python3 -m venv myproject`

`source myproject/bin/activate`

### Install build package:
You need it to convert your project to a wheel package.

`python3 -m pip install build`

### Install twine package:
This tool is needed to transfer your package to the pypi.org website.

`python3 -m pip install twine`

### Create your account on test.pypi.org and pypi.org:
[test.pypi.org](https://test.pypi.org/) is a test environment to make sure the [pypi.org](https://pypi.org/) would be kept clean.
You need to create an account on both sites.
For more information about using token to login, read on [Api Token](https://pypi.org/help/#apitoken)

`nano ~/.pypirc`
```
[testpypi]
username = __token__
password = (past yor token hear)

[pypi]
username = __token__
password = (past yor token hear)

```


### on root folder:

`python3 -m build`

It crates a dir name dist and add two files. Naming is a combination of package name and current version.
Name and version can be set in setup.py or setup.cfg file. In this tutorial we use setup.py.


