#include <Python.h>
#include <stdint.h>


/*
Levenshtein edit distance calculated via Myers bit-parallel algorithm

G. Myers (1999) A Fast Bit-Vector Algorithm for Approximate String Matching
Based on Dynamic Programming, Journal of the ACM: 495-415.
*/
static int64_t myers(uint8_t *t, int64_t n, uint8_t *p, int64_t m) {
    uint64_t pv, mv;        // positive and negative vertical delta values
    uint64_t ph, mh;        // positive and negative horizontal delta values
    uint64_t xv, xh;        // current vertical and horizontal states
    uint64_t eq, hb, peq[256];
    int64_t score =  m;
    uint8_t i, j;

    // populate lookup table
    memset(peq, 0, sizeof(peq));
    for (i=0; i<m; i++) {
        peq[p[i]] |= (uint64_t) 1 << i;
    }

    // set initial values
    pv = (uint64_t) - 1;
    mv = (uint64_t) 0;
    hb = (uint64_t) 1 << (m - 1);
    
    for (j=0; j<n; j++) {
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
        ph = (ph << 1);
        pv = (mh << 1) | ~ (xv | ph);
        mv = ph & xv;
    }
    return score;
}


static PyObject* turboshtein_levenshtein(PyObject *self, PyObject *args) {
    PyObject *w1, *w2;
    int64_t l1, l2;

    if (!PyArg_ParseTuple(args, "UU", &w1, &w2)) {
        return NULL;
    }

    l1 = PyUnicode_GET_LENGTH(w1);
    l2 = PyUnicode_GET_LENGTH(w2);

    if (l1 > 63 || l2 > 63) {
        PyErr_SetString(PyExc_ValueError, "input string(s) are too long.");
    }

    if (l1 <= l2) {
        return PyLong_FromLongLong(
            myers(
                PyUnicode_DATA(w1), l1,
                PyUnicode_DATA(w2), l2
            )
        );
    }

    else {
        return PyLong_FromLongLong(
            myers(
                PyUnicode_DATA(w2), l2,
                PyUnicode_DATA(w1), l1
            )
        );
    }
}


PyDoc_STRVAR(levenshtein_doc,
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
    "   1. Both strings must consist of exclusively ascii characters.\n"
    "   2. Input string lengths must be less than 64 characters each.\n"
    "\n"
    "[1] Gene Myers. 1999. A fast bit-vector algorithm for approximate string\n"
    "matching based on dynamic programming. J. ACM 46, 3 (May 1999), 395-415.\n"
    "https://doi.org/10.1145/316542.316550\n"
    "\n"
);


static PyMethodDef turboshtein_methods[] = {
    {
        "levenshtein",
        turboshtein_levenshtein,
        METH_VARARGS,
        levenshtein_doc
    },
    {
        NULL,
        NULL,
        0,
        NULL
    }
};


static struct PyModuleDef turboshtein_definition = {
    PyModuleDef_HEAD_INIT,
    "turboshtein", 
    "Fast Levenshtein edit distance calculations in Python",
    -1,
    turboshtein_methods
};


PyMODINIT_FUNC PyInit_turboshtein(void) {
    return PyModule_Create(&turboshtein_definition);
};
