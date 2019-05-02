def turn(p1, p2, p3):
    vector_1 = (p3[0] - p1[0], p3[1] - p1[1])
    vector_2 = (p2[0] - p1[0], p2[1] - p1[1])
    return vector_1[0] * vector_2[1] - vector_2[0] * vector_1[1]

def distance(p1, p2):
    return (p2[0] - p1[0]) * (p2[0] - p1[0]) + (p2[1] - p1[1]) * (p2[1] - p1[1])