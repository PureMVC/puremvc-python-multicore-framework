## [PureMVC](http://puremvc.github.com/) Python MultiCore Framework [![Python package](https://github.com/PureMVC/puremvc-python-multicore-framework/actions/workflows/python-package.yml/badge.svg)](https://github.com/PureMVC/puremvc-python-multicore-framework/actions/workflows/python-package.yml)

PureMVC is a lightweight framework for creating applications based upon the classic [Model-View-Controller](http://en.wikipedia.org/wiki/Model-view-controller) design meta-pattern. It supports [modular programming](http://en.wikipedia.org/wiki/Modular_programming) through the use of [Multiton](http://en.wikipedia.org/wiki/Multiton) Core actors instead of the [Singleton](http://en.wikipedia.org/wiki/Singleton_pattern)s used in the [Standard Version](https://github.com/PureMVC/puremvc-python-standard-framework/wiki).

* [PyPI Package](https://pypi.org/project/PureMVC/)
* [API Docs](https://puremvc.org/pages/docs/Python/multicore)
* [Legacy Implementation](https://github.com/PureMVC/puremvc-python-multicore-framework/tree/1.0.1)

# Installation

```commandline
pip install PureMVC
```
<!---
Development: pip install -e .
Testing: pytest test/
Build: python -m build
Publish: twine upload dist/*

Documentation: Generate
mkdir docs && cd docs && sphinx-quickstart --sep -p PureMVC -a "Saad Shams" -v "2.0.0" -r "BSD 3-Clause License" -l "en"
cd ../ && sphinx-apidoc -o docs/source src/puremvc && cd docs && make html && open build/html/index.html && cd ..

Documentation: Update
sphinx-apidoc -o docs/source src/puremvc --force && cd docs && make html && open build/html/index.html && cd ..

conf.py
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
extensions = ['sphinx.ext.autodoc']
html_theme = 'sphinx_rtd_theme'

index.rst
13: modules
-->

## Status
Production - [Version 2.0.1](https://github.com/PureMVC/puremvc-python-multicore-framework/blob/master/VERSION)

## Platforms / Technologies
* [Python](http://en.wikipedia.org/wiki/Python_(programming_language))
* [NumPy](https://numpy.org)
* [Pandas](https://pandas.pydata.org)
* [TensorFlow](https://www.tensorflow.org)
* [PyTorch](https://pytorch.org)

## Reference

* [PythonWheels](https://pythonwheels.com)
* [Classifiers](https://pypi.org/classifiers/)
* [Sphinx Documentation](https://www.sphinx-doc.org/en/master/index.html)
* [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html)

## License
* PureMVC MultiCore Framework for Python - Copyright © 2025 [Saad Shams](https://www.linkedin.com/in/muizz/)
* PureMVC - Copyright © 2025 [Futurescale, Inc.](http://futurescale.com/)
* All rights reserved.

* Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
  * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
  * Neither the name of Futurescale, Inc., PureMVC.org, nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
