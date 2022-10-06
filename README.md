# turboshtein

[![gh-actions-ci](https://img.shields.io/github/workflow/status/nathanrooy/turboshtein/ci?style=flat-square)](https://github.com/nathanrooy/turboshtein/actions?query=workflow%3Aci)
[![GitHub license](https://img.shields.io/github/license/nathanrooy/turboshtein?style=flat-square)](https://github.com/nathanrooy/turboshtein/blob/master/LICENSE)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/turboshtein.svg?style=flat-square)](https://pypi.org/pypi/turboshtein/)
[![PyPi Version](https://img.shields.io/pypi/v/turboshtein.svg?style=flat-square)](https://pypi.org/project/turboshtein)

## Background
I didn't study computer science so [bitwise operations](https://en.wikipedia.org/wiki/Bitwise_operation) have always been a bit of a gray area for me. I finally gave in and decided to spend some time reading up on the subject and ended up implementing the Myers bit-parallel algorithm<sup>[[1](https://github.com/nathanrooy/turboshtein#references)]</sup> for computing [Levenshtein edit distance](https://en.wikipedia.org/wiki/Levenshtein_distance). I was fairly happy with the results so I wrapped the original C code in Python and uploaded it to PyPI. Coincidentally, it's also pretty fast.

## Usage
Install via PyPI:

```sh
pip install turboshtein
```

Or not:
```
python setup.py install
```

Computing levenshtein edit distance between two strings:
```py
>>> from turboshtein import levenshtein
>>> levenshtein("saturday", "sunday")
3
```

Note that there are several limitations, mainly:
- Max string length must be less than 64.
- ASCII characters only.

## Performance
Values represent the number of string pairs processed per second.

|                                 library | version |     m=n=8 |    m=n=16 |    m=n=24 |    m=n=32 |    m=n=40 |    m=n=48 |    m=n=56 |
|----------------------------------------:|--------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
|                 turboshtein.levenshtein |   0.0.4 | 7,625,612 | 6,134,367 | 5,160,757 | 4,455,692 | 3,897,966 | 3,477,885 | 3,147,237 |
| [Levenshtein.distance](https://github.com/maxbachmann/Levenshtein) |  0.20.5 | 6,448,035 | 5,335,239 | 4,556,680 | 4,034,226 | 3,550,695 | 3,211,664 | 2,910,581 |
| [rapidfuzz.distance.Levenshtein.distance](https://github.com/maxbachmann/RapidFuzz) |  2.11.1 | 6,446,954 | 5,268,454 | 4,560,213 | 4,027,110 | 3,540,574 | 3,215,206 | 2,912,386 |
| [jellyfish.levenshtein_distance](https://github.com/jamesturk/jellyfish) |   0.9.0 | 3,823,843 | 1,494,087 |   718,785 |   399,693 |   262,541 |   183,554 |   135,081 |
| [textdistance.levenshtein](https://github.com/life4/textdistance) |   4.5.0 |   444,305 |   413,950 |   411,441 |   401,539 |   395,777 |   389,462 |   385,233 |

Test setup:
- XPS 15 9570
- Intel i7-8750H
- Fedora Linux 36 (Workstation Edition)

## References
[1]: Gene Myers. 1999. A fast bit-vector algorithm for approximate string matching based on dynamic programming. J. ACM 46, 3 (May 1999), 395-415. https://doi.org/10.1145/316542.316550
