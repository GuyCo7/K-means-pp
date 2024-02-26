import sys


DEFAULT_ITERATIONS = 300


def main():
    
    # Step 1: Reading user CMD arguments
    
    if len(sys.argv) > 6 or len(sys.argv) < 5:
        print("Please Enter 5 or 6 arguments")
        exit()
    
    k = convert_to_number(sys.argv[1])
    
    if len(sys.argv):
        iter = convert_to_number(sys.argv[2])
        eps = convert_to_number(sys.argv[3])
        file_name_1 = sys.argv[4]
        file_name_2 = sys.argv[5]
    else:
        iter = DEFAULT_ITERATIONS
        eps = convert_to_number(sys.argv[2])
        file_name_1 = sys.argv[3]
        file_name_2 = sys.argv[4]
    
    
    assert k > 1, "Invalid number of clusters!"
    assert iter > 1 and iter < 1000, "Invalid number of iteration!"
    
    
    # Step 2: Combine both input files by inner join using the first column in each file as a key
    
    text_file_1 = open(file_name_1, 'r')
    raw_text_1 = text_file_1.read()
    text_file_1.close()
    text_file_2 = open(file_name_2, 'r')
    raw_text_2 = text_file_2.read()
    text_file_2.close()

    # TODO: inner join 
    
    
    
    
    # Step 3: Sort the data points by the ’key’ in ascending order
    
    
        



# ~~~ Helper Functions ~~~

# Function to convert a string to int
def convert_to_number(str):
    try:
        return int(str)
    except ValueError:
        print(str + " is not a whole number!")
        print("Check your arguments again")
        exit()

if __name__ == "__main__":
    main()