from scamp import *
import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools

# C = 0
# A 440 = 69

def dist_mod12(x, y):
    return min(abs(x-y), abs(x+12-y))

class PitchSet:
    # a set of pitches, invariant to inversions but not transpositions to new key
    # since inversion-invariant, we will choose to list in order starting from C
    # maybe make a static class to call on lists...
    
    def __init__(self, pitches): #takes in a list of pitches
        self.pitches = set(pitches) # remove duplicates
        self.pitches = sorted([p % 12 for p in self.pitches])
        self.n = len(self.pitches)

    def issubset(self, other):
        return set(shift_pitches) <= set(other.pitches)

    def equiv(self, other):
        return self.pitches == other.pitches

    def dist(self, other):
        pass

    def generate_neighbor_sets(self, distance):
        #only simple harmonies please...
        # neighbors in high-dimensional balls grow exponentially
        neighbors = []
        step_sizes = [-2, -1, 1, 2] # small steps for efficient voice leading
        steps = [-2, -1, 1, 2]
        if distance == 0:
            return []
        elif distance == 1:
            steps = [(s, ) for s in steps]
        else:
            for _ in range(distance - 1):
                steps = list(itertools.product(steps, step_sizes))
        samples = list(itertools.combinations(range(self.n), distance))

        for sample in samples:
            for step in steps:
                neighbor = self.pitches.copy()
                for d in range(distance):
                    i, s = sample[d], step[d]
                    neighbor[i] += s
                neighbors.append(PitchSet(neighbor))
        return neighbors

    def __repr__(self):
        return str(self.pitches)

    ## instead of randomly generating stepwise motion, we may instead build a labeled graph
 ## of allowed transitions to other pitch sets
    ## this can be converted back to linear motion between chords

class PitchSetGraph:
    def get_node_color(self, name):
        if 'maj' in name:
            return 'lightgreen'
        elif 'min' in name:
            return 'crimson'
        else:
            raise ValueError('not major or minor')
        
    def __init__(self, pitch_sets, labeldict=None):
        self.dist2color = {1: 'magenta', 2: 'blue'}
        self.G = nx.Graph()
        for ps in pitch_sets:
            self.G.add_node(ps)
        if labeldict:
            self.labeldict = labeldict
            for ps in pitch_sets:
                name = labeldict[ps]
                self.G.nodes[ps]['color'] = self.get_node_color(name)
            
        for u in self.G.nodes:
            self.connect_neighbors(u)

    def connect_neighbors(self, u):
        for d in self.dist2color.keys():
            candidates = u.generate_neighbor_sets(d)
            for v in candidates:
                for w in self.G.nodes:
                    if v.equiv(w):
                        self.G.add_edge(u, w, weight=d, color=self.dist2color[d])
                        break

    def draw(self):
        nodes,node_colors = zip(*nx.get_node_attributes(self.G,'color').items())
        edges,edge_colors = zip(*nx.get_edge_attributes(self.G,'color').items())
        nx.draw_shell(self.G,
                with_labels=True,
                labels=self.labeldict,
                nodelist=nodes,
                node_color=node_colors,
                node_size = 1200,
                edgelist=edges,
                edge_color=edge_colors,
                font_size=10,
                font_weight='bold',
                width=2)
        plt.show()  

    def get_random_cycle(self, start_node=None, end_node=None, length=float('inf')):
        if start_node is None:
            start_node = random.choice(list(self.G.nodes))
        prev_node = start_node
        cycle = [start_node]
        ## I think I need to change the probabilities...
        # there are far more neighbors at distance 2
        # however, melodically we should try to use lower distance chords more often.
        while True:
            node = random.choice(list(self.G.neighbors(prev_node)))
            cycle.append(node)
            if node == start_node:
                break
            else:
                prev_node = node
        return cycle

# useful subroutines: calculating dissonance score
# calculating pairing between two chords (which voice moves where). Or maybe just annotate on the edge.
# harmonize a moving line
