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


static PyMethodDef turboshtein_methods[] = {
    {
        "levenshtein",
        turboshtein_levenshtein,
        METH_VARARGS,
        "Levenshtein edit distance between two ascii strings"
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
