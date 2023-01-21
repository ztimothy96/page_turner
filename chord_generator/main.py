from chord_gen import *

c_major = PitchSet([0, 4, 7])
neighbors = c_major.generate_neighbor_sets(2)

triads = [ #pesky human naming conventions
    [0, 4, 7],
    [1, 5, 8],
    [2, 6, 9],
    [3, 7, 10],
    [4, 8, 11],
    [5, 9, 0],
    [6, 10, 1],
    [7, 11, 2],
    [8, 0, 3],
    [9, 1, 4],
    [10, 2, 5],
    [11, 3, 6],
    [0, 3, 7],
    [1, 4, 8],
    [2, 5, 9],
    [3, 6, 10],
    [4, 7, 11],
    [5, 8, 0],
    [6, 9, 1],
    [7, 10, 2],
    [8, 11, 3],
    [9, 0, 4],
    [10, 1, 5],
    [11, 2, 6]]
for i in range(len(triads)):
    triads[i] = PitchSet(triads[i])
labeldict = {}
names = ['C maj',
         'C# maj',
         'D maj',
         'Eb maj',
         'E maj',
         'F maj',
         'F# maj',
         'G maj',
         'Ab maj',
         'A maj',
         'Bb maj',
         'B maj',
         'C min',
         'C# min',
         'D min',
         'Eb min',
         'E min',
         'F min',
         'F# min',
         'G min',
         'G# min',
         'A min',
         'Bb min',
         'B min']
for i in range(len(triads)):
    labeldict[triads[i]] = names[i]
    
triad_graph = PitchSetGraph(triads, labeldict=labeldict)
triad_graph.draw()
cycle = triad_graph.get_random_cycle()
print([labeldict[v] for v in cycle])
