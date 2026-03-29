#define PY_SSIZE_T_CLEAN
#include "Python.h"

static PyObject* encode(PyObject* self, PyObject* args) {
    const char* message;
    Py_ssize_t len_message;
    PyObject* encoded;
    Py_ssize_t i, j, idx, jdx;
    int c, b, existing_value;

    if (!PyArg_ParseTuple(args, "s#", &message, &len_message)) {
        return NULL;
    }

    encoded = PyList_New(len_message);
    if (!encoded) {
        return NULL;
    }

    for (i = 0; i < len_message; i++) {
        idx = ((i * 79) + 2) % len_message;
        c = (int)message[idx];
        existing_value = 0;
        for (j = 7; j >= 0; j--) {
            jdx = ((j * 3) + 6) % 8;
            b = ((c >> j) & 1) << jdx;
            existing_value ^= b;
        }
        PyList_SetItem(encoded, i, PyLong_FromLong(existing_value));
    }

    return encoded;
}

static PyMethodDef methods[] = {
    {"encode", encode, METH_VARARGS, "Encode message."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "encode",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC PyInit_encode(void) {
    return PyModule_Create(&module);
}