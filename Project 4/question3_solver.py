from math import sqrt
class Question3_Solver:
    def __init__(self):
        self.initCentroids = [(30, 30), (150, 30), (90, 130)]
        return;

    def getDistance(self, pointA, pointB):
        X1, Y1 = pointA
        X2, Y2 = pointB
        return sqrt(((X1 -X2) **2) + ((Y1 -Y2) **2))

    def getMinDistCluster (self, point, centroids):
        minDist = 9999999
        idx = -1

        for i, centroid in zip(range(len(centroids)), centroids):
            dist = self.getDistance(point, centroid)
            if dist < minDist:
                minDist = dist
                idx = i

        return idx

    def getMean(self, List):
        Xsum = Ysum = 0
        for (X, Y) in List:
            Xsum += X
            Ysum += Y

        Xmean = Xsum /len(List)
        Ymean = Ysum /len(List)

        return (Xmean, Ymean)

    def compareTwoLists (self, List1, List2):
        if len(List1) != len(List2):
            return False

        for i, j in zip(List1, List2):
            if i != j:
                return False

        return True

    # Add your code here.
    # Return the centroids of clusters.
    # You must use [(30, 30), (150, 30), (90, 130)] as initial centroids
    def solve(self, points):
        lcentroids = self.initCentroids
        prev1 = [0 for i in range(3)]
        prev2 = [0 for i in range(3)]

        while True:
            if self.compareTwoLists(prev1, prev2) and self.compareTwoLists(prev2, lcentroids):
                break

            cluster = [[] for x in range(3)]
            for point in points:
                cluster[self.getMinDistCluster(point, lcentroids)].append(point)

            for i in range(3):
                lcentroids[i] = self.getMean(cluster[i])

            prev2 = list(prev1)
            prev1 = list(lcentroids)

        return lcentroids