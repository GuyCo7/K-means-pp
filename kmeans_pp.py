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
    
    # print ("1:::::\n" + table1.to_string())
    # print ("2:::::\n" + table2.to_string())

    merged_table = pd.merge(table1, table2, on=0)
    d = merged_table.shape[1] - 1
    
    # Step 3: After join, sort the data points by the ’key’ in ascending order.
    
    sorted_table = merged_table.sort_values(by=0)
    
    # Step 4: Implementation of the k-means++ algorithm
    # Kmeans++ Implementation
    
    # 1 - Choose one center uniformly at random among the data points.
    N = len(sorted_table)
    
    assert k < N, "Invalid number of clusters!"
    
    np.random.seed(0)
    first_centeroid_index = np.random.choice(N)
    print("first_center_index --- " + str(first_centeroid_index))
    
    first_center_centroid = sorted_table.values[first_centeroid_index]
    print(first_center_centroid)
    
    centroids = [first_center_centroid[1:]]
    print("centroids --- " + str(centroids))
    
    
    # 4 - Repeat Steps 2 and 3 until k centers have been chosen
    while len(centroids) < k:
        
    # 2 - For each data point x not chosen yet, compute D(x), the distance between x and the nearest
    #     center that has already been chosen.
        # centroids_indices = [centroid[0] for centroid in centroids]
        # for i in range(N):
        #     if i in centroids_indices:
        #         print(str(i) + " is inside the centroids list")
        #         continue
            # min_distance = D(sorted_table.values[i][1:], [centroid[1:] for centroid in centroids])
            # print(min_distance)
            # distance = euclidean_distance(sorted_table.values[i][1:], sorted_table.values[first_centeroid_index][1:])
            # print(distance)
            
        
        # 3 - Choose one new data point at random as a new center, using a weighted probability distribution
        #     where a point x is chosen with probability proportional to P(xl)
        
        
        probabilities = get_probabilities(sorted_table, N, centroids)
        # print("probabilities - " + str(probabilities))
        # print("number of elements --- " + str(len(probabilities)))
        # sum = 0
        # for prob in probabilities:
        #     sum += prob
        
        # print("sum --- " + str(sum))
        
        chosen_index = np.random.choice(range(N), p=probabilities)
        # print("chosen --- " + str(chosen_index))
        
        chosen_centroid = sorted_table.values[chosen_index]
        print("chosen_centroid[1:] ---" + str(chosen_centroid[1:]))
        centroids.append(chosen_centroid[1:])
        print("centroids --- " + str(centroids))
    
    # print("number of centroids --- " + str(len(centroids)))
    # print("k --- " + str(k))
    
    # 5 - Now that the initial centers have been chosen, proceed using standard k-means clustering

    data_point = []
    for i in range(N):
        data_point.append(sorted_table.values[1:])
        
    final_centroids = kmeans_capi.kmeans(k, iter, N, d, eps, centroids, data_point)
    
    
    final_centroid_indices = [centroid[0] for centroid in final_centroids]
    print(str(final_centroid_indices))
    for centroid in final_centroids:
        print (str(centroid[1:]))


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