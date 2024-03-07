#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *kmeans(PyObject *self, PyObject *args)
{
    int k;
    int iter;
    int n;
    int dimension;
    /* This parses the Python arguments into a double (d)  variable named z and int (i) variable named n*/
    if (!PyArg_ParseTuple(args, "iiii", &k, &iter, &n, &dimension))
    {
        return NULL; /* In the CPython API, a NULL value is never valid for a
                        PyObject* so it is used to signal that an error has occurred. */
    }

    // TODO: change "d" to ret value (void?)
    // TODO: use kmeans from HW1
    /* This builds the answer ("d" = Convert a C double to a Python floating point number) back into a python object */
    return Py_BuildValue("d", kmeans(k, iter, n, dimension)); /*  Py_BuildValue(...) returns a PyObject*  */
}

static PyMethodDef kmeansMethods[] = {
    {"kmeans",                   /* the Python method name that will be used */
     (PyCFunction)kmeans,        /* the C-function that implements the Python function and returns static PyObject*  */
     METH_VARARGS,               /* flags indicating parameters
                                    accepted for this function */
     PyDoc_STR("kmeans in c.")}, /* The docstring for the function */
    {NULL, NULL, 0, NULL}        /* The last entry must be all NULL as shown to act as a
                                    sentinel. Python looks for this entry to know that all
                                    of the functions for the module have been defined. */
};

static struct PyModuleDef kmeansmodule = {
    PyModuleDef_HEAD_INIT,
    "kmeans_capi", /* name of module */
    NULL,          /* module documentation, may be NULL */
    -1,            /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    kmeansMethods  /* the PyMethodDef array from before containing the methods of the extension */
};

PyMODINIT_FUNC PyInit_kmeans_capi(void)
{
    PyObject *m;
    m = PyModule_Create(&kmeansmodule);
    if (!m)
    {
        return NULL;
    }
    return m;
}