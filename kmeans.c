#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "cap.h"

double **kmeans_c(int k, int iter, int N, int d, double eps, double **centroids, double **vectors_arr)
{
    // double **vectors_arr;
    int i, j;
    int count = 0;
    // double **centroids;
    int *closest_centroid_for_vector;
    int iteration = 0;
    double *delta_centroids;
    int point_index;
    double closest_centroid_distance;
    int centroid_index;
    double curr_d;
    double *sum;
    double *new_centroid;

    closest_centroid_for_vector = (int *)malloc(N * sizeof(int));
    if (closest_centroid_for_vector == NULL)
    {
        printf("An Error Has Occurred\n");
        return NULL;
    }
    for (i = 0; i < N; i++)
    {
        double min_distance = distance(vectors_arr[i], centroids[0], d);
        closest_centroid_for_vector[i] = 0;
        for (j = 1; j < k; j++)
        {
            double curr_distance = distance(vectors_arr[i], centroids[j], d);
            if (curr_distance < min_distance)
            {
                closest_centroid_for_vector[i] = j;
                min_distance = curr_distance;
            }
        }
    }

    delta_centroids = (double *)malloc(k * sizeof(double));
    if (delta_centroids == NULL)
    {
        printf("An Error Has Occurred\n");
        free(closest_centroid_for_vector);
        return NULL;
    }
    for (i = 0; i < k; i++)
    {
        delta_centroids[i] = 1.0;
    }

    sum = (double *)malloc(d * sizeof(double));
    if (sum == NULL)
    {
        printf("An Error Has Occurred\n");
        free(delta_centroids);
        free(closest_centroid_for_vector);
        return NULL;
    }
    for (i = 0; i < d; i++)
    {
        sum[i] = 0.0;
    }

    new_centroid = (double *)malloc(d * sizeof(double));
    if (new_centroid == NULL)
    {
        printf("An Error Has Occurred\n");
        free(sum);
        free(delta_centroids);
        free(closest_centroid_for_vector);
        return NULL;
    }
    for (i = 0; i < d; i++)
    {
        new_centroid[i] = 0.0;
    }

    while (areBiggerThanEpsilon(delta_centroids, k, eps) && iteration < iter)
    {
        for (point_index = 0; point_index < N; point_index++)
        {
            closest_centroid_distance = distance(vectors_arr[point_index], centroids[closest_centroid_for_vector[point_index]], d);
            for (centroid_index = 0; centroid_index < k; centroid_index++)
            {
                curr_d = distance(vectors_arr[point_index], centroids[centroid_index], d);
                if (curr_d < closest_centroid_distance)
                {
                    closest_centroid_for_vector[point_index] = centroid_index;
                    closest_centroid_distance = curr_d;
                }
            }
        }
        for (centroid_index = 0; centroid_index < k; centroid_index++)
        {
            for (i = 0; i < d; i++)
            {
                sum[i] = 0.0;
            }
            for (i = 0; i < d; i++)
            {
                new_centroid[i] = 0.0;
            }
            count = 0;
            for (i = 0; i < N; i++)
            {
                if (closest_centroid_for_vector[i] == centroid_index)
                {
                    count++;
                    for (j = 0; j < d; j++)
                    {
                        sum[j] += vectors_arr[i][j];
                    }
                }
            }
            for (j = 0; j < d; j++)
            {
                new_centroid[j] = sum[j] / count;
            }
            delta_centroids[centroid_index] = distance(centroids[centroid_index], new_centroid, d);
            for (i = 0; i < d; i++)
            {
                centroids[centroid_index][i] = new_centroid[i];
            }
        }
        iteration++;
    }

    /* Print centroids */
    for (i = 0; i < k; i++)
    {
        for (j = 0; j < d; j++)
        {
            printf("%.4f", centroids[i][j]);
            if (j < d - 1)
            {
                printf(",");
            }
            else
            {
                printf("\n");
            }
        }
    }

    /* Free allocated memory */

    free(closest_centroid_for_vector);
    free(delta_centroids);
    free(sum);
    free(new_centroid);

    return centroids;
}

// Helper Functions

double distance(double *point1, double *point2, int d)
{
    double sum = 0.0;
    int i;
    for (i = 0; i < d; i++)
    {
        sum += pow(point1[i] - point2[i], 2);
    }
    return sqrt(sum);
}

int areBiggerThanEpsilon(double *arr, int size, double eps)
{
    int i;
    for (i = 0; i < size; i++)
    {
        if (arr[i] > eps)
        {
            return 1;
        }
    }
    return 0;
}

int isInteger(char *str)
{
    char *endptr;
    strtol(str, &endptr, 10);
    if (*endptr != '\0' || endptr == str)
    {
        return 0;
    }
    return 1;
}
