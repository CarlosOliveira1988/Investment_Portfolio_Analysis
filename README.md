[![](https://img.shields.io/static/v1?label=python&message=3.9&color=blue&logo=python)](https://docs.python.org/3/whatsnew/3.9.html)
[![](https://img.shields.io/static/v1?label=code%20style&message=black&color=black&logo=black)](https://github.com/psf/black)
[![](https://img.shields.io/static/v1?label=linter&message=pylint&color=green&logo=pylint)](https://github.com/PyCQA/pylint)
[![](https://img.shields.io/static/v1?label=security&message=bandit&color=yellow&logo=bandit)](https://github.com/PyCQA/bandit)
[![](https://img.shields.io/static/v1?label=testing&message=pytest&color=green&logo=pytest)](https://docs.pytest.org/en/latest/)

# **Investment_Portfolio_Analysis**

This repository is useful to perform some financial analysis in Investment Portfolio.

---

## **Installation**

Run the command `pip install -r requirements.txt` to install Python packages using the file [requirements.txt](requirements.txt) there's in repository.

Always that a new package is necessarily to run the project, it's necessary to include it in the file [requirements.txt](requirements.txt).

See below how it works.

### **How it works**

We use the `pip` to install the Python packages to use in projects.

All official Python packages are in [PyPI (The Python Package Index)](https://pypi.org/), but it's possible to install unofficial packages from others locals.

To easy the project packages management we use the file [requirements.txt](requirements.txt) that list all base packages to run the project.

Some examples:

```properties
# We can install unofficial packages from GitHub if we want a package that there's not on PyPI or when we need a library in development or even a fork instead of traditional version.
-e git+https://github.com/jtemporal/caipyra.git@master#egg=caipyra
# We can pin a package version to guarantee the project operation avoiding problems with others versions.
seaborn==0.8.1
# We can determine a minimum package version that contain the minimum features required in project.
pandas>=0.18.1
# We can determine a range of package versions that project works correctly.
pandas-datareader>=0.8.0,<=0.10.0
# We can determine to use always the last package version.
serenata-toolbox
```

See the full docs [on this link](https://pip.pypa.io/en/stable/cli/pip_install/#requirements-file-format).
