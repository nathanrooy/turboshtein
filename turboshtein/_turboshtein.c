#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdint.h>
#include <string.h>

/*
Levenshtein edit distance calculated via Myers bit-parallel algorithm

G. Myers (1999) A Fast Bit-Vector Algorithm for Approximate String Matching
Based on Dynamic Programming, Journal of the ACM: 395-415.
*/
static int64_t myers(const uint8_t *t, int64_t n, const uint8_t *p, int64_t m) {
  uint64_t pv, mv; // positive and negative vertical delta values
  uint64_t ph, mh; // positive and negative horizontal delta values
  uint64_t xv, xh; // current vertical and horizontal states
  uint64_t eq, hb;
  uint64_t peq[256];
  int64_t score = m;
  int64_t i, j;

  // populate lookup table
  memset(peq, 0, sizeof(peq));
  for (i = 0; i < m; i++) {
    peq[p[i]] |= (uint64_t)1 << i;
  }

  // set initial values
  pv = (uint64_t)-1;
  mv = (uint64_t)0;
  hb = (uint64_t)1 << (m - 1);

  for (j = 0; j < n; j++) {
    // bit vectors for reference symbol j
    eq = peq[t[j]];

    // compute current delta vector
    xv = eq | mv;
    xh = (((eq & pv) + pv) ^ pv) | eq;

    // update horizontal delta values
    ph = mv | ~(xh | pv);
    mh = pv & xh;

    // update score
    if (ph & hb) {
      score++;
    }

    if (mh & hb) {
      score--;
    }

    // update vertical delta values
    ph = (ph << 1) | 1;
    pv = (mh << 1) | ~(xv | ph);
    mv = ph & xv;
  }

  return score;
}

static PyObject *turboshtein_levenshtein(PyObject *self, PyObject *const *args,
                                         Py_ssize_t nargs) {
  if (nargs != 2) {
    PyErr_Format(PyExc_TypeError,
                 "levenshtein() takes exactly 2 arguments (%zd given)", nargs);
    return NULL;
  }

  PyObject *w1 = args[0];
  PyObject *w2 = args[1];

  if (!PyUnicode_Check(w1) || !PyUnicode_Check(w2)) {
    PyErr_SetString(PyExc_TypeError, "input arguments must be strings.");
    return NULL;
  }

  if (PyUnicode_KIND(w1) != PyUnicode_1BYTE_KIND ||
      PyUnicode_KIND(w2) != PyUnicode_1BYTE_KIND) {
    PyErr_SetString(PyExc_ValueError,
                    "input strings must contain only ASCII or Latin-1 characters.");
    return NULL;
  }

  Py_ssize_t l1 = PyUnicode_GET_LENGTH(w1);
  Py_ssize_t l2 = PyUnicode_GET_LENGTH(w2);

  if (l1 > 63 || l2 > 63) {
    PyErr_SetString(PyExc_ValueError, "input string(s) are too long.");
    return NULL;
  }

  if (w1 == w2) {
    return PyLong_FromLong(0);
  }

  const uint8_t *s1 = PyUnicode_1BYTE_DATA(w1);
  const uint8_t *s2 = PyUnicode_1BYTE_DATA(w2);

  // strip common prefix
  while (l1 > 0 && l2 > 0 && *s1 == *s2) {
    s1++;
    s2++;
    l1--;
    l2--;
  }

  // strip common suffix
  while (l1 > 0 && l2 > 0 && s1[l1 - 1] == s2[l2 - 1]) {
    l1--;
    l2--;
  }

  if (l1 == 0) {
    return PyLong_FromSsize_t(l2);
  }
  if (l2 == 0) {
    return PyLong_FromSsize_t(l1);
  }

  if (l1 <= l2) {
    return PyLong_FromLongLong(myers(s1, l1, s2, l2));
  } else {
    return PyLong_FromLongLong(myers(s2, l2, s1, l1));
  }
}

PyDoc_STRVAR(
    levenshtein_doc,
    "Computes the Levenshtein distance between two strings.\n"
    "\n"
    "Parameters\n"
    "----------\n"
    "a : str\n"
    "    first string\n"
    "b : str\n"
    "    second string\n"
    "\n"
    "Returns\n"
    "-------\n"
    "edit distance : int\n"
    "    The Levenshtein edit distance between strings `a` and `b`\n"
    "\n"
    "Examples\n"
    "--------\n"
    ">>> from turboshtein import levenshtein\n"
    ">>> levenshtein('saturday','sunday')\n"
    "3\n"
    "\n"
    "Notes\n"
    "-----\n"
    "This function utilizes the bit-vector algorithm developed by Myers[1]."
    "\nIt's very fast, but this implementation has a few limitations:\n"
    "   1. Both strings must consist of exclusively ascii or latin-1 characters.\n"
    "   2. Input string lengths must be less than 64 characters each.\n"
    "\n"
    "[1] Gene Myers. 1999. A fast bit-vector algorithm for approximate string\n"
    "matching based on dynamic programming. J. ACM 46, 3 (May 1999), 395-415.\n"
    "https://doi.org/10.1145/316542.316550\n"
    "\n");

static PyMethodDef turboshtein_methods[] = {
    {"levenshtein", (PyCFunction)turboshtein_levenshtein, METH_FASTCALL,
     levenshtein_doc},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef turboshtein_definition = {
    PyModuleDef_HEAD_INIT, "_turboshtein",
    "Fast Levenshtein edit distance calculations in Python", -1,
    turboshtein_methods};

PyMODINIT_FUNC PyInit__turboshtein(void) {
  return PyModule_Create(&turboshtein_definition);
}
