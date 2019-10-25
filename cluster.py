import sys
import csv
from decimal import *

train_file = sys.argv[1]
cluster_count_input = sys.argv[2]

cluster_count = int(cluster_count_input)

members = []
clusters = []
cluster = []

count = 0
R_count = 0
D_count = 0

# Load training data
data = csv.reader(open(train_file, newline=''), delimiter=',')
for row in data:
    votes = []
    for i in range (0,42):
        votes.append(row[i])
    members.append(votes)

# Fill cluster list with single members
for x in range(0,len(members)):
    cluster = [x]
    clusters.append(cluster)


# Compare each cluster and merge closest pair
while(len(clusters)>cluster_count):
    min_dist = 2  
    merge = [0] * 2
    for x in range (0,len(clusters)-1):
        for y in range (x+1,len(clusters)):
            x_count = len(clusters[x])
            y_count = len(clusters[y])
            links = Decimal(x_count * y_count)
            total_dist = Decimal(0)

            # Compare each member in cluster pair, calculate average distance
            for x_cluster in range (0,x_count):
                for y_cluster in range(0,y_count):
                    x_member = members[clusters[x][x_cluster]]
                    y_member = members[clusters[y][y_cluster]]
                    matches = 0

                    # Count matches to find the intersection
                    for c in range (0,42):
                        if(x_member[c]==y_member[c]):
                            matches+=1
                    distance = Decimal((2*42 - 2*matches)/(2*42-matches)) #The Jaccard distance (1-Jaccard index)
                    total_dist += distance
            avg_dist = total_dist/links
            
            # Save new min dist and the closest cluster pair
            if(avg_dist < min_dist):
                min_dist = avg_dist
                merge[0] = x
                merge[1] = y

    # Pop the two closest clusters, merge and append to clusters list
    x_merge = clusters.pop(merge[0])
    y_merge = clusters.pop(merge[1]-1)
    merged = y_merge + x_merge
    clusters.append(merged)

# Sort the clusters then the cluster list
for cl in clusters:
    cl.sort()

clusters.sort()

# Print the clusters
for clu in clusters:
    line = ', '.join(map(str,clu))
    print(line)




