class Question3_Solver:
    def __init__(self):
        self.initCentroids = [(30, 30), (150, 30), (90, 130)]
        return;

    def getMinDistCluster (self, point, centroids):
        minDist = -9999999
        minCentroid = (0, 0)
        idx = -1

        for i, centroid in map(range(len(centroids)), centroids):
            dist = self.getDistance (point, centroid)
            if dist > minDist:
                minDist = dist
                idx = i
                minCentroid = centroid

        return (i, minCentroid)

    # Add your code here.
    # Return the centroids of clusters.
    # You must use [(30, 30), (150, 30), (90, 130)] as initial centroids
    def solve(self, points):
        lcentroids = self.initCentroids
        prev1 = prev2 = None

        while True:
            prev2 = prev1
            prev1 = lcentroids
            if prev1 == prev2 and prev2 == lcentroids:
                break
                
            for point in points:
                (idx, (X, Y)) = self.getMinDistCluster (point, lcentroids)
                lcentroid[idx].append((X,Y))

        print lcentroids
        return lcentroids
