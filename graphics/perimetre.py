#
# 
# perimetre format
# [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
#
#
# feature format
# [type, subtype, subsubtype, offset, length, height1, height2, inward, inneroffset]
#
# types
# 1) feature
#
# 2) window
#
# 3) door
#     a) single
#         i) left
#        ii) right
#     b) double
#     c) sliding
#         i) left
#        ii) right
#
# 4) bay
#
# 5) radiator

import math


def initial_perim(length,width):
    myperimetre = []
    myperimetre.append([0, 0])
    myperimetre.append([length, 0])
    myperimetre.append([length,width])
    myperimetre.append([0,width])
    return myperimetre

def perimeter_length(myperimetre,upto_point):
    if (upto_point <= 0):
        array_length = len(myperimetre)
    else:
        array_length = upto_point
    length = [0,[]]
    n = 0
    while (n < array_length):
        if (array_length-1 > n):
            m = n
            #ittetrate over the array
        if (n == array_length-1):
            m = -1
            #The last array pair is back to 00
        # finds the distance between 2 coordinates 
        # adds that distance to the length variable
        (length[1]).append(math.dist((myperimetre[n]), (myperimetre[m+1])))
        length[0] = length[0] + (math.dist((myperimetre[n]), (myperimetre[m+1])))
        print("room wall: ", n+1, " wall length: ", math.dist((myperimetre[n]), (myperimetre[m+1])))
        n = n + 1
    return length

def direction_check(perimetre_coords,n):
    # for all but the last coordinate
    if (len(perimetre_coords)-1 > n):
        m = n
    # linking the last coordinate to [0,0]
    if (n == len(perimetre_coords)-1):
        m = -1
    
    #print("the x is different and y is same")
    if (((perimetre_coords[n])[0] != (perimetre_coords[m+1])[0]) and ((perimetre_coords[n])[1] == (perimetre_coords[m+1])[1])):
        # horizontal
        # right
        if ((perimetre_coords[n])[0] < (perimetre_coords[m+1])[0]):
            direction = [0,((0*math.pi)/2)]
            return direction
        # left
        if ((perimetre_coords[n])[0] > (perimetre_coords[m+1])[0]):
            direction = [4,((2*math.pi)/2)]
            return direction
    #print("the y is different and x is same")
    if (((perimetre_coords[n])[1] != (perimetre_coords[m+1])[1]) and ((perimetre_coords[n])[0] == (perimetre_coords[m+1])[0])):
        # veritcal
        # down
        if ((perimetre_coords[n])[1] < (perimetre_coords[m+1])[1]):
            direction = [2,((1*math.pi)/2)]
            return direction
        # up
        if ((perimetre_coords[n])[1] > (perimetre_coords[m+1])[1]):
            direction = [6,((3*math.pi)/2)]
            return direction
    #print("the x and y is different")
    if (((perimetre_coords[n])[0] != (perimetre_coords[m+1])[0]) and ((perimetre_coords[n])[1] != (perimetre_coords[m+1])[1])):
        # diagonal
        # right,down
        if (((perimetre_coords[n])[0] < (perimetre_coords[m+1])[0]) and ((perimetre_coords[n])[1] < (perimetre_coords[m+1])[1])):
            angle = math.atan(math.dist([(perimetre_coords[n])[1]], [(perimetre_coords[m+1])[1]])/math.dist([(perimetre_coords[n])[0]], [(perimetre_coords[m+1])[0]]))
            direction = [1,angle]
            return direction
        # right,up
        if (((perimetre_coords[n])[0] < (perimetre_coords[m+1])[0]) and ((perimetre_coords[n])[1] > (perimetre_coords[m+1])[1])):
            angle = math.atan((math.dist([(perimetre_coords[n])[1]],[(perimetre_coords[m+1])[1]]))/(math.dist([(perimetre_coords[n])[0]],[(perimetre_coords[m+1])[0]])))
            direction = [7,angle]
            return direction
        # left,down
        if (((perimetre_coords[n])[0] > (perimetre_coords[m+1])[0]) and ((perimetre_coords[n])[1] < (perimetre_coords[m+1])[1])):
            angle = math.atan((math.dist([(perimetre_coords[n])[1]],[(perimetre_coords[m+1])[1]]))/(math.dist([(perimetre_coords[n])[0]],[(perimetre_coords[m+1])[0]])))
            direction = [3,angle]
            return direction
        # left,up
        if (((perimetre_coords[n])[0] > (perimetre_coords[m+1])[0]) and ((perimetre_coords[n])[1] > (perimetre_coords[m+1])[1])):
            angle = math.atan((math.dist([(perimetre_coords[n])[1]],[(perimetre_coords[m+1])[1]]))/(math.dist([(perimetre_coords[n])[0]],[(perimetre_coords[m+1])[0]])))
            direction = [5,angle]
            return direction

def direction_words(direction):
    if (direction[0] == 0):
        print("left to right")
    if (direction[0] == 1):
        print("right down ", direction[1])
    if (direction[0] == 2):
        print("up to down")
    if (direction[0] == 3):
        print("left down ", direction[1])
    if (direction[0] == 4):
        print("right to left")
    if (direction[0] == 5):
        print("left up ", direction[1])
    if (direction[0] == 6):
        print("down to up")
    if (direction[0] == 7):
        print("right up ", direction[1])

def fit_check(feature,perimetre_coords):
    # feature[4] is a real number that represents the length of the feature that may be added.
    # this runs a while loop to check if the length of that feature fits between any of the coordinates in the perimetre.  
    n = 0
    fits = []
    while (n < len(perimetre_coords)):
        if (len(perimetre_coords)-1 > n):
        # this checks the distance between the current and next coordinate
        # and appends fits a 1 if the length does fit and a 0 if it doesnt
            m = n
        if (n == len(perimetre_coords)-1):
        # this checks the distance between the last coordinate and [0,0]
        # and appends fits a 1 if the length does fit and a 0 if it doesnt
            m = -1
        
        if (feature[4] >= math.dist((perimetre_coords[n]), (perimetre_coords[m+1]))):
            print("the length doesnt fit")
            fits.append(0)
        else:
            fits.append(1)
            direction = direction_check(perimetre_coords,n)
            direction_words(direction)
        n = n + 1

        # on the last loop it tells you which walls the feature will fit on
        if (n >= len(perimetre_coords)):
            m = 0
            while (m <= len(fits)-1):
                if (fits[m] > 0):
                    print("the feature fits on wall", m+1)
                m = m + 1
    return fits

def offset_length_fit_check(perimetre_coords,feature):
    target_offset = feature[3]
    walls = []
    n = 0
    if (len(perimetre_coords)-1 > n):
        m = n
    if (n == len(perimetre_coords)-1):
        m = -1
    while (target_offset+feature[4] > math.dist(perimetre_coords[n],perimetre_coords[m+1])):
        target_offset = target_offset - math.dist(perimetre_coords[n],perimetre_coords[m+1])
        walls.append(0)
        n = n + 1

        if (len(perimetre_coords)-1 > n):
            m = n
        if (n == len(perimetre_coords)-1):
            m = -1
    walls.append(1)
    walls_target_offset = [walls,target_offset]
    return walls_target_offset

def first_free_decider(walls,fits):
    n = 0
    for x in walls:
        if (x == 1):
            break
        n = n + 1
    
    first_free = False
    if (fits[n] == 0):
        while (fits[n] == 0):
            if (len(fits)-1 == n):
                n = 0
            else:
                n = n + 1
        first_free = True
    n_first_free = [n,first_free]
    return n_first_free

def axis_variables_setter(rotation_state,target_offset,feature,first_free):
    if (first_free == True):
        target_offset = 0

    if ((rotation_state == 0) or (rotation_state == 1)):
        target_offsetx = target_offset
        target_offsety = 0
        lengthx  = feature[4]
        lengthy  = 0
        height1x = 0
        height1y = feature[5]
        height2x = 0
        height2y = feature[6]
    if ((rotation_state == 2) or (rotation_state == 3)):
        target_offsetx = 0
        target_offsety = target_offset
        lengthx  = 0
        lengthy  = feature[4]
        height1x = feature[5]*-1
        height1y = 0
        height2x = feature[6]*-1
        height2y = 0
    if ((rotation_state == 4) or (rotation_state == 5)):
        target_offsetx = target_offset*-1
        target_offsety = 0
        lengthx  = feature[4]
        lengthy  = 0
        height1x = 0
        height1y = feature[5]*-1
        height2x = 0
        height2y = feature[6]*-1
    if ((rotation_state == 6) or (rotation_state == 7)):
        target_offsetx = 0
        target_offsety = target_offset*-1
        lengthx  = 0
        lengthy  = feature[4]*-1
        height1x = feature[5]
        height1y = 0
        height2x = feature[6]
        height2y = 0
    target_offset   = [target_offsetx,target_offsety]
    length          = [lengthx,lengthy]
    height1         = [height1x,height1y]
    height2         = [height2x,height2y]
    trgt_lngth_hght1_hght2 = [target_offset,length,height1,height2]
    return trgt_lngth_hght1_hght2

def rotation_trig(perimetre_coords,n,target_offset,length,height1,height2,rotation):
    rotation_list = [[],[],[],[]]
    rotation_list[0].append((perimetre_coords[n])[0]+target_offset[0]  +(target_offset[0]*math.sin(rotation)))
    rotation_list[0].append((perimetre_coords[n])[1]+target_offset[1]  +(target_offset[1]*math.cos(rotation)))
    rotation_list[1].append((perimetre_coords[n])[0]+target_offset[0]+height1[0]  +(target_offset[0]*math.sin(rotation)))
    rotation_list[1].append((perimetre_coords[n])[1]+target_offset[1]+height1[1]  +(target_offset[1]*math.cos(rotation)))
    rotation_list[2].append((perimetre_coords[n])[0]+target_offset[0]+height2[0]+length[0]  +(target_offset[0]*math.sin(rotation)))
    rotation_list[2].append((perimetre_coords[n])[1]+target_offset[1]+height2[1]+length[1]  +(target_offset[1]*math.cos(rotation)))
    rotation_list[3].append((perimetre_coords[n])[0]+target_offset[0]+length[0]  +(target_offset[0]*math.sin(rotation)))
    rotation_list[3].append((perimetre_coords[n])[1]+target_offset[1]+length[1]  +(target_offset[1]*math.cos(rotation)))
    #feature_coords = list(set(rotation_list))
    feature_Coords = []
    for item in rotation_list:
        if item not in feature_Coords:
            feature_Coords.append(item)
    return feature_Coords

def remove_duplicates(perimetre_coords):
    n1 = 0
    while (len(perimetre_coords) > n1):
        n2 = 0
        while (len(perimetre_coords) > n2):
            if (n1 == n2):
                n2 = n1 + 1
            if (n2 == len(perimetre_coords)):
                break
            if (perimetre_coords[n1] == perimetre_coords[n2]):
                perimetre_coords.pop(n1)
                perimetre_coords.pop(n2-1)
            n2 = n2 + 1
        n1 = n1 + 1

def feature_coords(feature,perimetre_coords):
    #feature = [typelist, subtype, subsubtype, offset, length, height1, height2, inward, inneroffset, name, leadingto]
    
    fits = fit_check(feature,perimetre_coords)
    n = 0
    sum = 0
    while (n < len(fits)):
        sum = sum + fits[n]
        n = n + 1
    if (sum != 0):
        print("it can start drawing the feature")

        walls_target_offset = offset_length_fit_check(perimetre_coords,feature)
        walls = walls_target_offset[0]
        target_offset = walls_target_offset[1]

        n_first_free = first_free_decider(walls,fits)
        n = n_first_free[0]
        first_free = n_first_free[1]

        if (fits[n] == 1):
            direction = direction_check(perimetre_coords,n)
            direction_words(direction)
            
            rotation_state = direction[0]
            rotation = direction[1]
            trgt_lngth_hght1_hght2 = axis_variables_setter(rotation_state,target_offset,feature,first_free)
            target_offset   = trgt_lngth_hght1_hght2[0]
            length          = trgt_lngth_hght1_hght2[1]
            height1         = trgt_lngth_hght1_hght2[2]
            height2         = trgt_lngth_hght1_hght2[3]

            feature_Coords = rotation_trig(perimetre_coords,n,target_offset,length,height1,height2,rotation)

            m = 0
            while (len(feature_Coords) > m):
                xy1 = feature_Coords[m]
                perimetre_coords.insert(n+1,xy1)
                n = n + 1
                m = m + 1
            remove_duplicates(perimetre_coords)
        
        print("hfgierg")
        #perimetre_coords.insert()
        #perimeter_length(perimetre_coords,upto_point)



        



    



box = [10,10]
perimetre_coords=initial_perim(box[0],box[1])
print (perimetre_coords)
perimetre_length=perimeter_length(perimetre_coords,0)
print("room perimetre: ", perimetre_length[0])

n = 0
features = [[0, 0, 0, 7, 3, 0, 4, 0, 0, "triangle feature thing1", ""]
           ,[0, 0, 0, 8, 1, 1, 1, 0, 0, "triangle feature thing2", ""]]
#features = [[0, 0, 0, 3, 2, 3, 1, 0, 0, "triangle feature thing1", ""]]
#features = [[0, 0, 0, 3, 2, 3, 3, 0, 0, "triangle feature thing1", ""]
#           ,[0, 0, 0, 7, 1, 1, 1, 0, 0, "triangle feature thing2", ""]]
while (n < len(features)):
    if ((features[n])[0] == 0):
        print("the feature is a triangle or rectangle thing")
        passed = feature_coords(features[n],perimetre_coords)
    print (perimetre_coords)

    n = n + 1

print (perimetre_coords)
print(perimeter_length(perimetre_coords,0))



#feature = [typelist, subtype, subsubtype, offset, length, height1, height2, inward, inneroffset, name, leadingto]


