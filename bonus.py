import matplotlib.pyplot as plt
from sklearn import datasets

def main():
    
    
    for k in range(1, 11):
        # TODO: run kmeans++
        # kmeans(k, /.....)
        
        # TODO: compute inertia
        # inertia(k)
        
        pass
        
    
    # TODO: plot all 10 inertias
    # plt.plot(k, inertia, kind=)

    return 0

        
def inertia(N, vectors, centroids):
    sum = 0
    for i in range(N):
        current_vector = vectors[i]
        relevant_centroid = get_centroid_for_vector(vectors[i])
        
        sum += difference_squared(current_vector, relevant_centroid)
        
    return sum
        



# ~~~ Helper Functions ~~~

def difference_squared(vector_x, vector_y):
    sum = 0
    for i in range(len(vector_x)):
        sum += (float(vector_x[i]) - float(vector_y[i])) ** 2
    
    return sum

# returns the relevant centroid for the vector
def get_centroid_for_vector(vector, centroids):
    return
    

if __name__ == "__main__":
    main()