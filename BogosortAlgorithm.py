# Python program for implementation of Bogo Sort
import random

# Sorts array a[0..n-1] using Bogo sort
def bogoSort(a):
    n = len(a)

    global tryCount
    tryCount = 0

    while (is_sorted(a)== False):
        tryCount += 1
        print("Attempt Failed.")
        shuffle(a)
 
# To check if array is sorted or not
def is_sorted(a):
    n = len(a)
    for i in range(0, n-1):
        if (a[i] > a[i+1] ):
            return False
    return True
 
# To generate permutation of the array
def shuffle(a):
    n = len(a)
    for i in range (0,n):
        r = random.randint(0,n-1)
        a[i], a[r] = a[r], a[i]
 
# Driver code to test above
a = []
listSize = 10
for i in range(listSize):
    a.append(random.randint(1,50))

bogoSort(a)
print("Sorted array :")
for i in range(len(a)):
    print ("%d" %a[i]),
print("This action took " + str(tryCount) + " Attempts")