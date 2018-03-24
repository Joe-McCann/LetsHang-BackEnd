import math

l2norm = lambda x,y: math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

def centroid(points):
    x = sum([points[x][0] for x in range(len(points))])/len(points)
    y = sum([points[x][1] for x in range(len(points))])/len(points)
    return (x, y)

def geoMean(points, gamma, iters):

    guess = centroid(points)
    tot = 0
    for rep in range(0, iters):
        gradient = [0, 0]
        
        for point in points:

            gradient[0] += (guess[0]-point[0])/(l2norm(guess, point))
            gradient[1] += (guess[1]-point[1])/(l2norm(guess, point))

        guess = (guess[0]-gamma*gradient[0], guess[1]-gamma*gradient[1])

    return guess

def minSig(points, gamma, iters):
    guess = centroid(points)
    for rep in range(0, iters):
        gradient = [0, 0]
        vals = [0, 0, 0]
        for point in points:
            demon = (l2norm(guess, point))
            vals[0]+=demon
            vals[1]+=(guess[0]-point[0])/demon
            vals[2]+=(guess[1]-point[1])/demon
        vals = [vals[i]/len(points) for i in range(0,3)]
        
        for point in points:
            demon = (math.sqrt((guess[0]-point[0])**2+(guess[1]-point[1])**2))
            gradient[0] += (demon-vals[0])*((guess[0]-point[0])/demon-vals[1])
            gradient[1] += (demon-vals[0])*((guess[1]-point[1])/demon-vals[2])
        guess = (guess[0]-gamma*2/(len(points)-1)*gradient[0], guess[1]-gamma*2/(len(points)-1)*gradient[1])
    return guess
