from utilis import distance
from config import distance_ok
def is_index_up(hand):
    tip = hand[8]
    pip = hand[6]
    return tip.y<pip.y
def is_thumb_up(hand, hand_label):
    if hand_label == "Right":
        return hand[4].x < hand[3].x

    return hand[4].x > hand[3].x
def finger_state(hand, hand_label):
    fingers= []
    # index
    fingers.append(int(is_thumb_up(hand, hand_label)))
    fingers.append(int(hand[8].y < hand[6].y))
    # Middle
    fingers.append(int(hand[12].y < hand[10].y))
    # Ring
    fingers.append(int(hand[16].y < hand[14].y))
    # Pinky
    fingers.append(int(hand[20].y < hand[18].y))

    return fingers

# gestures
Gestures = {
    (1,1,1,1,1):"Open Palm",
    (0,0,0,0,0):"Fist",
    (0,1,0,0,0):"Pointing",
    (0,1,1,0,0):"Victory",
    (0,1,1,1,0):"Scroll"
}
def recognize_gesture(hand, hand_label):
    states = finger_state(hand, hand_label)
    if distance(hand,4,8) < distance_ok:
        return "OK"
    return Gestures.get(tuple(states), "unknown")


    