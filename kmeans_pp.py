import math
import sys
import pandas as pd
import numpy as np
import kmeans_capi

DEFAULT_ITERATIONS = 300


def main():
    
    # Step 1: Reading user CMD arguments
    
    if len(sys.argv) > 6 or len(sys.argv) < 5:
        print("Please Enter 5 or 6 arguments")
        exit()
    
    k = convert_to_number(sys.argv[1])
    
    if len(sys.argv) == 6:
        iter = convert_to_number(sys.argv[2])
        eps = convert_to_float(sys.argv[3])
        file_name_1 = sys.argv[4]
        file_name_2 = sys.argv[5]
    else:
        iter = DEFAULT_ITERATIONS
        eps = convert_to_float(sys.argv[2])
        file_name_1 = sys.argv[3]
        file_name_2 = sys.argv[4]
    
    
    assert k > 1, "Invalid number of clusters!"
    assert iter > 1 and iter < 1000, "Invalid number of iteration!"
    
    
    # Step 2: Combine both input files by inner join using the first column in each file as a key
    
    table1 = pd.read_csv(file_name_1, header=None)
    table2 = pd.read_csv(file_name_2, header=None)
    
    table1.columns = range(table1.shape[1])
    table2.columns = range(table2.shape[1])

    merged_table = pd.merge(table1, table2, on=0)
    d = merged_table.shape[1] - 1
    
    
    # Step 3: After join, sort the data points by the ’key’ in ascending order.
    
    sorted_table = merged_table.sort_values(by=0)
    
    N = len(sorted_table)
    assert k < N, "Invalid number of clusters!"
    
    
    # Step 4: Implementation of the k-means++ algorithm
    # Kmeans++ Implementation
    
    # 1 - Choose one center uniformly at random among the data points.
    
    np.random.seed(0)
    first_centeroid_index = np.random.choice(N)
    centroids_indices = [first_centeroid_index]
    
    first_centroid = sorted_table.values[first_centeroid_index][1:].tolist()
    centroids = [first_centroid]    
    
    # 4 - Repeat Steps 2 and 3 until k centers have been chosen
    while len(centroids) < k:
        
    # 2 - For each data point x not chosen yet, compute D(x), the distance between x and the nearest
    #     center that has already been chosen.
    # 3 - Choose one new data point at random as a new center, using a weighted probability distribution
    #     where a point x is chosen with probability proportional to P(xl)
        
        
        probabilities = get_probabilities(sorted_table, N, centroids)
        
        chosen_centeroid_index = np.random.choice(N, p=probabilities)
        
        centroids_indices.append(chosen_centeroid_index)
        chosen_centroid = sorted_table.values[chosen_centeroid_index][1:].tolist()
        centroids.append(chosen_centroid)
    
    # 5 - Now that the initial centers have been chosen, proceed using standard k-means clustering

    # Parsing the vectors from pandas data frame to a 2D list and cutting the index of each vector
    data_points = []
    for i in range(N):
        data_points.append(sorted_table.values[i][1:].tolist())
    
    # Calling the kmeans C API with all the required params
    final_centroids = kmeans_capi.fit(k, iter, N, d, eps, centroids, data_points)
    
    # Print the output
    print(",".join([str(index) for index in centroids_indices]))
    for centroid in final_centroids:
        formatted_centroid = ",".join(["{:.4f}".format(coordination) for coordination in centroid])
        print(formatted_centroid)
    
    


# ~~~ Helper Functions ~~~

# Function to convert a string to int
def convert_to_number(str):
    try:
        return int(str)
    except ValueError:
        print(str + " is not a whole number!")
        print("Check your arguments again")
        exit()

def convert_to_float(str):
    try:
        return float(str)
    except ValueError:
        print(str + " is not a float!")
        print("Check your arguments again")
        exit()

# Function to calculate Euclidean distance
def euclidean_distance(vector_x, vector_y):
    sum = 0
    for i in range(len(vector_x)):
        sum += (float(vector_x[i]) - float(vector_y[i])) ** 2
    
    return math.sqrt(sum)


def get_probability(vector, centroids, vectors, N):
    current_min_distance = D(vector, centroids)
    
    sum = 0
    for i in range(N):
        current_vector = vectors[i][1:]
        sum += D(current_vector, centroids)
    
    return current_min_distance / sum


def get_probabilities(sorted_table, N, centroids):
    probabilities = []
    for i in range(N):
        current_vector = sorted_table.values[i][1:]
        current_probability = get_probability(current_vector, centroids, sorted_table.values, N)
        probabilities.append(current_probability)
    
    return probabilities
    

def D(vector, centroids):
    distances = [euclidean_distance(vector, centroid) for centroid in centroids]
    return min(distances)
    
if __name__ == "__main__":
    main()