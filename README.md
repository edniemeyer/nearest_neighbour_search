# Nearest Neighbours Search
## Goal
Given a list of trucks and their current locations and a list of cargos and their pickup and delivery
locations, *find the optimal mapping of trucks to cargos to minimize the overall distances
the trucks must travel.*

## About the solution
I've implemented 2 algorithms to solve this Nearest Neighbour problem. Notice that for the positions of trucks and cargos we've considered a cartesian approach for distances to make it simpler. To be real, we should have used a haversine formula to find the nearest ones, but that wouldn't be possible with Kd trees. A more real approach would be to use the BallTree algorithm with haversine formula.

The first is the brute force algorithm, where we compute all distances between points in both datasets. For each target point, it has a time complexity of O(DN) where D is the number of dimensions (in this case, 2). For small datasets it can be pretty fast and doesn't need to lose time by building a tree, which happens in the next solution. Also, it is not a good approach to find the next closest ones, as it can skip the next closest if it finds **the** closest first. This is needed when there are repeated closests for the cargos.

The second solution is by using the Kd-tree algorithm. To build the Kd-tree, we need O(DN log N) where D is the number of dimensions (2). To search for the nearest point to a target one on the tree, it has a time complexity of O(log N), which is a great improvement over the brute force method for higher dimensions and bigger datasets. It also has the ability to find the next K nearest neighbours(KNN), which is necessary on this problem, as there are reapeated trucks found to be the nearest for the same cargo.

It was also necessary to implement a recursive algorithm to find the next closest truck, when there are repeated ones found for different cargos. In this case, we have to make sure the next closest is not a repeated one as well, compare the distances for the next closest, and finally choose the best scenario.

## Usage 
### Installation

Only default packages from **Python 3.8.2** were used. There is no need to install anything else, just make sure to have the mentioned version of Python installed ([Virtual Env recommended](https://docs.python.org/3/library/venv.html)).

### Main
To run the script and find the optimal mapping of trucks to cargos:
```bash
python3 -m main brute
```
*or*
```bash
python3 -m main kdtree
```
### Tests
To run tests:
```bash
python3 -m unittest
```