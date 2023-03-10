import csv
import math

# Function to calculate distance between two sets of latitude and longitude coordinates
def location_distance(lat1, lon1, lat2, lon2):
    R = 6371e3
    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))
    delta_phi = math.radians(float(lat2) - float(lat1))
    delta_lambda = math.radians(float(lon2) - float(lon1))

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

# Function to calculate Levenshtein distance between two strings
def levenshtein_distance(s1, s2):
    m = len(s1)
    n = len(s2)
    # Create a 2D list of size (m+1)x(n+1) and initialize it with 0s
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    # Fill in the values of the 2D list
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])

    # Return the value at the bottom-right corner of the 2D list
    return dp[m][n]

# Function to check if two names are similar
def is_similar_name(name1, name2):
    # Two names are considered similar if their Levenshtein distance is less than or equal to 5
    return levenshtein_distance(name1, name2) <= 5

data = []

# Read the dataset from a CSV file and store it in a list of lists
with open('dataset.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # skip header row
    # Append a new column to the header row to indicate if two names are similar
    header.append('is_similar')
    for row in reader:
        data.append(row)

results = []

# Iterate over each pair of rows in the dataset
for i in range(len(data)):
    #check for duplicacy
    if(i>0 and len(results)>0 and data[i]==results[len(results)-1][:3]):
        continue
    flag=0
    for j in range(i + 1, len(data)):
        name1, lat1, lon1 = data[i]
        name2, lat2, lon2 = data[j]

        # Calculate the distance between the two sets of latitude and longitude coordinates
        distance = location_distance(lat1, lon1, lat2, lon2)

        # Check if the distance is less than or equal to 200 meters and if the two names are similar
        if distance <= 200 and is_similar_name(name1, name2):
            #if match is found set flag=1
            flag=1
            # Append the two rows to the results list along with a new column indicating that the two names are similar
            results.append(data[i] + [1])
            results.append(data[j] + [1])
        
    #if match is not found , add the row with is_similar 0
    if flag==0:
        results.append(data[i] + [0])



# Write the results to a new CSV file
with open('results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(results)
