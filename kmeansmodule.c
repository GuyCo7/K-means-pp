#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "cap.h"

static PyObject *kmeans(PyObject *self, PyObject *args)
{
    int i;
    int j;
    int k;
    int iter;
    int n;
    int d;
    double eps;
    double **centroids;
    double **vectors_arr;
    double **parsed_centroids;
    double **result_centroids;
    double **parsed_vectors;
    PyObject *py_value;
    PyObject *cen_value;
    double num;

    /* Parse Python arguments */
    if (!PyArg_ParseTuple(args, "iiiidOO", &k, &iter, &n, &d, &eps, &centroids, &vectors_arr))
    {
        return NULL;
    }

    // Allocate memory for the vectors array of pointers to doubles
    parsed_vectors = (double **)malloc(n * sizeof(double *));
    if (parsed_vectors == NULL)
    {
        printf("Error: Memory allocation failed\n");
        return NULL;
    }

    for (i = 0; i < n; i++)
    {
        parsed_vectors[i] = (double *)malloc(d * sizeof(double));
        if (parsed_vectors[i] == NULL)
        {
            printf("An Error Has Occurred\n");
            for (j = 0; j < i; j++)
            {
                free(vectors_arr[j]);
            }
            free(vectors_arr);
            return NULL;
        }
    }

    // Allocate memory for the vectors array of pointers to doubles
    parsed_centroids = (double **)malloc(k * sizeof(double *));
    if (parsed_centroids == NULL)
    {
        printf("Error: Memory allocation failed\n");
        return NULL;
    }

    for (i = 0; i < k; i++)
    {
        parsed_centroids[i] = (double *)malloc(d * sizeof(double));
        if (parsed_centroids[i] == NULL)
        {
            printf("An Error Has Occurred\n");
            for (j = 0; j < i; j++)
            {
                free(parsed_centroids[j]);
            }
            free(parsed_centroids);
            return NULL;
        }
    }

    for (i = 0; i < n; i++)
    {
        for (j = 0; j < d; j++)
        {
            py_value = PyList_GetItem(PyList_GetItem(vectors_arr, i), j);
            num = PyFloat_AsDouble(py_value);
            parsed_vectors[i][j] = num;
            if (i < k)
            {
                cen_value = PyList_GetItem(PyList_GetItem(centroids, i), j);
                num = PyFloat_AsDouble(cen_value);
                parsed_centroids[i][j] = num;
            }
        }
    }

    // print vectors
    // for (i = 0; i < k; i++)
    // {
    //     for (j = 0; j < d; j++)
    //     {
    //         printf("%.4f", parsed_vectors[i][j]);
    //         if (j < d - 1)
    //         {
    //             printf(",");
    //         }
    //         else
    //         {
    //             printf("\n");
    //         }
    //     }
    // }

    result_centroids = kmeans_c(k, iter, n, d, eps, parsed_centroids, parsed_vectors);
    free(parsed_centroids);
    free(parsed_vectors);

    return Py_BuildValue("O", result_centroids); /*  Py_BuildValue(...) returns a PyObject*  */
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