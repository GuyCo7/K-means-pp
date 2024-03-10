#ifndef CAP_H
#define CAP_H

double **kmeans_c(int k, int iter, int N, int d, double eps, double **centroids, double **vectors_arr);
double distance(double *point1, double *point2, int d);
int areBiggerThanEpsilon(double *arr, int size, double eps);
int isInteger(char *str);

#endif