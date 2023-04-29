#Import stuff
import random
import time

def sort(array):
    #Sort array with Quicksort

    less = []
    equal = []
    greater = []

    #Organizaion based on pivot value
    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            elif x > pivot:
                greater.append(x)
        
        #Return the values
        return sort(less)+equal+sort(greater) #Use plus operator to join lists
    #You want Equal ---->^^^^^^ not pivot
    else:
        return array

#Create a random list 
a = []
listSize = 10
for i in range(listSize):
    a.append(random.randint(1, 9))

#Starts the clock
startTime = round(time.time())

#Sort our list
sortedList = sort(a)

#Format it
print("Sorted array :")
for i in range(len(sortedList)):
    print ("%d" %sortedList[i]),
print("This action took " + str(round(time.time()) - startTime) + " Seconds")



