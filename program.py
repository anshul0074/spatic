import csv
from geopy.distance import geodesic

# Function to calculate distance between two sets of latitude and longitude coordinates
def location_distance(lat1, lon1, lat2, lon2):
    # Convert the input values to float
    coord1 = (float(lat1), float(lon1))
    coord2 = (float(lat2), float(lon2))
    # Calculate the geodesic distance between the two coordinates in meters
    distance = geodesic(coord1, coord2).meters
    return distance

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
    for j in range(i + 1, len(data)):
        name1, lat1, lon1 = data[i]
        name2, lat2, lon2 = data[j]

        # Calculate the distance between the two sets of latitude and longitude coordinates
        distance = location_distance(lat1, lon1, lat2, lon2)

        # Check if the distance is less than or equal to 200 meters and if the two names are similar
        if distance <= 200 and is_similar_name(name1, name2):
            # Append the two rows to the results list along with a new column indicating that the two names are similar
            results.append(data[i] + [1])
            results.append(data[j] + [1])
            #add empty line between each pair for readability (if not required then comment next line)
            results.append([])

# Write the results to a new CSV file
with open('results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(results)
