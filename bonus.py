from sklearn import datasets
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import math

def main():
    
    iris = datasets.load_iris()
    vectors = iris.data

    inertias = []    
    for k in range(1, 11):
        kmeans = KMeans(k, init="k-means++", random_state=0).fit(vectors)
        
        centroids = kmeans.cluster_centers_
        
        # Calc the inertia
        iner = inertia(vectors, centroids)
        inertias.append(iner)
        
    # Plot all 10 inertias and save to "elbow.png"

    plt.plot(range(1,11), inertias, marker="o")
    plt.title("Elbow Method for selection of optimal K clusters")
    plt.xlabel("K")
    plt.ylabel("Inertia")
    
    # On NOVA Server you must change "text=" to "s="
    plt.annotate(s="elbow point", xy=(2, inertias[1]), xytext=(2+1, inertias[1]+1), arrowprops=dict(facecolor='black', linestyle="--", linewidth=1))
    
    plt.savefig("elbow.png")

    return 0

def inertia(vectors, centroids):
    sum = 0
    for i in range(len(vectors)):
        current_vector = vectors[i]
        relevant_centroid = get_centroid_for_vector(vectors[i], centroids)
        
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
    distances = [euclidean_distance(vector, centroid) for centroid in centroids]
    min_distance = min(distances)
    index = distances.index(min_distance)
    return centroids[index]

# Function to calculate Euclidean distance
def euclidean_distance(vector_x, vector_y):
    sum = 0
    for i in range(len(vector_x)):
        sum += (float(vector_x[i]) - float(vector_y[i])) ** 2
    
    return math.sqrt(sum)
    

if __name__ == "__main__":
    main()