import numpy as np

class KMclustering(object):
    """
    Object for k-means clustering.

    TODO: accept an arbitrary distance definition,
    and swap that out for the defaul L2 distance
    used in _optimize_once().

    Note: the assignments object specifies which mean
    a point belongs to. This isn't absolutely necessary
    and can be gotten rid of if space must be optimized.
    """

    def __init__(self, points, k, distance_def = None):
        self.k = k
        self.points = points
        inds = np.arange(len(points))
        self.centers = np.random.choice(inds, k, replace = False)
        self.assignments = np.zeros(len(points))
        
    def _optimize_once(self):
        """
        Explaination: distances are identified using the L2-norm,
        or the Euclidean distance. The closest point is the
        one with the minimum L2-norm away from the source.
        """
        #Do the algo here
        #Update assignments
        for i, p in enumerate(self.points):
            d2max = np.inf
            for j, c in enumerate(self.centers):
                #L2 distance between point p and center c
                d2 = (p - self.points[c]) @ (p - self.points[c]) #dot product
                if d2 < d2max:
                    self.assignments[i] = j
                    d2max = d2
        
        #Find the new means
        #Take the mean for only the points assigned to
        #the i-th center.
        means = np.array(
            [np.mean(self.points[self.assignments == i], 0)
             for i in range(self.k)]
        )
        
        #Find the new center points based on the new means
        new_centers = np.zeros_like(self.centers)
        for i, m in enumerate(means):
            d2max = np.inf
            for j, p in enumerate(self.points):
                d2 = (m - p) @ (m - p)
                if d2 < d2max:
                    new_centers[i] = j
                    d2max = d2
        return new_centers

    def optimize(self):
        """
        Optimize the k centers by finding the mean of the
        assigned points and comparing that to the current assignments.
        Continue if they are different.
        """
        niter = 0 #number of iterations
        while True:
            niter += 1
            new_centers = self._optimize_once()
            if np.all(np.equal(new_centers, self.centers)):
                break
            else:
                self.centers = new_centers
        print(f"stopped after {niter} iterations")
        return

if __name__ == "__main__":
    N = 1000
    ndim = 2
    samples = np.random.rand(N, ndim)
    k = 4
    KMC = KMclustering(samples, k)
    KMC.optimize()
