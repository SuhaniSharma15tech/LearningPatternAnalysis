# # convert the csv to a 2 dimensional array
# import pandas as pd
# import numpy as np
# import random
# df=pd.read_csv("dimensionallyReduced.csv")
# data=df.to_numpy()



# # generate  the centroid coordinates for first iteration
#     # this should be an array too
#     # will improve on it later but for now let's just have 5 clusters
# K=5
#     # do i want 5 one dimensional arrays with 7 elems each
#     # or do i want a 2 dimensional array with 5 elements
#     # lets see how things go with the 2 dimensional array
#     # how do i generate the centroids of this stage?
#     # randomly generate or study data and then calculates variance and then start with some smart values
#     # for experimenting i will start with random generation
#     # will use k-Means++ for this later on for now just doing things with random datapoints
#     # pick 5 random datapoint
# li=[]
# for i in range(5):
#     li.append(data[random.randint(0,data.shape[0])])
# centroids=np.array(li)


# # define the function for euclidean distance
#     #  write this function for numpy arrays
# def distance(a1,a2):
#     p=np.subtract(a1,a2)
#     distance=0
#     for i in range(7):
#         distance+=p[i]**2
#     return distance



# # function to calculate coordinates of centroid of a cluster using datapoints that belong to that cluster
#     #  bring us a formula
#     # i assume we will have an array for it, like we will have an array of all datapoints belonging to that cluster
# def backtrack(arr):
#     return np.mean(arr,axis=0)
#     # this output array is our centroid for n+1 stage


# # make a function that says which all datapoints a cluster has (like store all datapoints of a cluster in some structure)
#     # how can you improve this step
#     # takes a number after comparison of  distances from all 5 centroids
#     # like we can have a list which stores distance of datapoint from all centroids
#     # we do this a=that_list.index(min(that_list))+1
#     # this a would serve as the index of cluster it belongs to
# clustered_data={1:[],2:[],3:[],4:[],5:[],6:[]}
# def clustering(a,datapoint):
#     global clustered_data[a].append(datapoint)

# # define the function that executes the algorithm 

# while True:
#     for i in data:
#         dis_list=[]
#         for j in centroids:
#             # calculate distance
#             dis_list.append(distance(i,j))
#         # do  the clustering
#         clustering(dis_list,i)
#     # check whether to stop or not

#     # calibrate centroids for next step
    

    

    

# # use tolerance or maybe put all those functions inside a loop to effectively control when to stop
# # if i go with tolerance what should exactly be the value for tolerance
# # i have one idea
# # you compare the centroids from last 3-4 stage in this way
# # how close are centroids of k and k-1 stage and then k-1 stage and k-2 stage
 
# # after the loop stops you want a csv or text file storing your  final centroids so that file should be the output of your function or code

