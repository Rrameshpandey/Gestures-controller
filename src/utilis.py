import numpy as np

def distance(hand,id1,id2):
    p1 = np.array([hand[id1].x, hand[id1].y])
    p2 = np.array([hand[id2].x, hand[id2].y])

    return np.linalg.norm(p2-p1)
    