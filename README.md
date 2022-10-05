# turboshtein

[![gh-actions-ci](https://img.shields.io/github/workflow/status/nathanrooy/turboshtein/ci?style=flat-square)](https://github.com/nathanrooy/turboshtein/actions?query=workflow%3Aci)
[![GitHub license](https://img.shields.io/github/license/nathanrooy/turboshtein?style=flat-square)](https://github.com/nathanrooy/turboshtein/blob/master/LICENSE)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/turboshtein.svg?style=flat-square)](https://pypi.org/pypi/turboshtein/)
[![PyPi Version](https://img.shields.io/pypi/v/turboshtein.svg?style=flat-square)](https://pypi.org/project/turboshtein)

## Background
I didn't study computer science so bitwise operations have always been a bit of a gray area for me. I finally gave in and decided to spend some time reading up on the subject and ended up implementing the Myers bit-parallel algorithm for computing Levenshtein edit distance. I was fairly happy with the results so I wrapped the original C code in Python and uploaded it to PyPI. Coincidentally, it's also pretty fast.

## Usage
Install via PyPI:

```sh
pip install turboshtein
```

Or not
```
python setup.py install
```

Computing levenshtein edit distance between two strings:
```sh
>>> From turboshtein import levenshtein
>>> levenshtein("saturday", "sunday")
3
```

Note that there are several limitations, mainly:
- Max string length must be less than 64.
- ASCII characters only.

## Performance
Values represent the number of string pairs processed per second.

|                                 library |     m=n=8 |    m=n=16 |    m=n=24 |    m=n=32 |    m=n=40 |    m=n=48 |    m=n=56 |
|----------------------------------------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
|                 turboshtein.levenshtein | 7,307,254 | 5,841,998 | 4,898,786 | 4,381,383 | 3,787,679 | 3,460,706 | 3,098,978 |
| rapidfuzz.distance.Levenshtein.distance | 6,115,119 | 5,000,410 | 4,430,285 | 3,895,723 | 3,313,308 | 3,132,127 | 2,732,176 |
|          jellyfish.levenshtein_distance | 5,726,999 | 4,930,084 | 4,329,111 | 3,814,256 | 3,119,216 | 3,090,797 | 2,727,032 |
|                    Levenshtein.distance | 3,725,694 | 1,389,628 |   710,292 |   389,632 |   249,694 |   180,106 |   131,543 |
|                textdistance.levenshtein |   407,845 |   393,642 |   371,919 |   375,995 |   374,140 |   374,889 |   359,589 |

Test setup:
- XPS 15 9570
- Intel i7-8750H
- Fedora Linux 36 (Workstation Edition)

## References
- Gene Myers. 1999. A fast bit-vector algorithm for approximate string matching based on dynamic programming. J. ACM 46, 3 (May 1999), 395-415. https://doi.org/10.1145/316542.316550
