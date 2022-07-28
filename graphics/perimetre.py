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

from __future__ import division
from copy import copy
import math
import json
from re import U

def initial_perim(length,width):
    """
    perimetre_coords = []
    perimetre_coords.append([0, 0])
    perimetre_coords.append([length, 0])
    perimetre_coords.append([length,width])
    perimetre_coords.append([0,width])"""

    walls_feature = [0, 0, 0, 0, length, width, width, 0, 0, "walls", ""]

    return walls_feature

def perimetre_length(perimetre_coords,upto_point):
    if (upto_point <= 0):
        array_length = len(perimetre_coords)
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
        distance = round(math.dist((perimetre_coords[n]), (perimetre_coords[m+1])),5)
        (length[1]).append(distance)
        length[0] = length[0] + (distance)
        print("room wall: ", n+1, " wall length: ", (distance))
        n = n + 1
    return length

def direction_check(perimetre_coords,n):
    # for all but the last coordinate
    if (len(perimetre_coords)-1 > n):
        m = n+1
    # linking the last coordinate to [0,0]
    if ((n == len(perimetre_coords)-1) or (len(perimetre_coords) == 1)):
        m = 0
    if (n == len(perimetre_coords)):
        n = 0
        m = n + 1
    #special case where x and y is the same
    if (((perimetre_coords[n])[0] == (perimetre_coords[m])[0]) and ((perimetre_coords[n])[1] == (perimetre_coords[m])[1])):
        direction = [0,((0*math.pi)/2)]
        return direction


    #print("the x is different and y is same")
    if (((perimetre_coords[n])[0] != (perimetre_coords[m])[0]) and ((perimetre_coords[n])[1] == (perimetre_coords[m])[1])):
        # horizontal
        # right
        if ((perimetre_coords[n])[0] < (perimetre_coords[m])[0]):
            direction = [0,((0*math.pi)/2)]
            return direction
        # left
        if ((perimetre_coords[n])[0] > (perimetre_coords[m])[0]):
            direction = [4,((2*math.pi)/2)]
            return direction
    #print("the y is different and x is same")
    if (((perimetre_coords[n])[1] != (perimetre_coords[m])[1]) and ((perimetre_coords[n])[0] == (perimetre_coords[m])[0])):
        # veritcal
        # down
        if ((perimetre_coords[n])[1] < (perimetre_coords[m])[1]):
            direction = [2,((1*math.pi)/2)]
            return direction
        # up
        if ((perimetre_coords[n])[1] > (perimetre_coords[m])[1]):
            direction = [6,((3*math.pi)/2)]
            return direction
    #print("the x and y is different")
    if (((perimetre_coords[n])[0] != (perimetre_coords[m])[0]) and ((perimetre_coords[n])[1] != (perimetre_coords[m])[1])):
        # diagonal
        # right,down
        if (((perimetre_coords[n])[0] < (perimetre_coords[m])[0]) and ((perimetre_coords[n])[1] < (perimetre_coords[m])[1])):
            angle = math.atan(math.dist([(perimetre_coords[n])[1]], [(perimetre_coords[m])[1]])/math.dist([(perimetre_coords[n])[0]], [(perimetre_coords[m])[0]]))
            direction = [1,angle]
            return direction
        # right,up
        if (((perimetre_coords[n])[0] < (perimetre_coords[m])[0]) and ((perimetre_coords[n])[1] > (perimetre_coords[m])[1])):
            angle = math.atan((math.dist([(perimetre_coords[n])[1]],[(perimetre_coords[m])[1]]))/(math.dist([(perimetre_coords[n])[0]],[(perimetre_coords[m])[0]])))
            direction = [7,angle]
            return direction
        # left,down
        if (((perimetre_coords[n])[0] > (perimetre_coords[m])[0]) and ((perimetre_coords[n])[1] < (perimetre_coords[m])[1])):
            angle = math.atan((math.dist([(perimetre_coords[n])[1]],[(perimetre_coords[m])[1]]))/(math.dist([(perimetre_coords[n])[0]],[(perimetre_coords[m])[0]])))
            direction = [3,angle]
            return direction
        # left,up
        if (((perimetre_coords[n])[0] > (perimetre_coords[m])[0]) and ((perimetre_coords[n])[1] > (perimetre_coords[m])[1])):
            angle = math.atan((math.dist([(perimetre_coords[n])[1]],[(perimetre_coords[m])[1]]))/(math.dist([(perimetre_coords[n])[0]],[(perimetre_coords[m])[0]])))
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

def axis_variables_setter(rotation_state,target_offset,feature,first_free,rotation):
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
        rotation = rotation - ((0*math.pi)/4)
    if ((rotation_state == 2) or (rotation_state == 3)):
        target_offsetx = 0
        target_offsety = target_offset
        lengthx  = 0
        lengthy  = feature[4]
        height1x = feature[5]*-1
        height1y = 0
        height2x = feature[6]*-1
        height2y = 0
        rotation = rotation - ((1*math.pi)/4)
    if ((rotation_state == 4) or (rotation_state == 5)):
        target_offsetx = target_offset*-1
        target_offsety = 0
        lengthx  = feature[4]
        lengthy  = 0
        height1x = 0
        height1y = feature[5]*-1
        height2x = 0
        height2y = feature[6]*-1
        rotation = rotation - ((2*math.pi)/4)
    if ((rotation_state == 6) or (rotation_state == 7)):
        target_offsetx = 0
        target_offsety = target_offset*-1
        lengthx  = 0
        lengthy  = feature[4]*-1
        height1x = feature[5]
        height1y = 0
        height2x = feature[6]
        height2y = 0
        rotation = rotation - ((4*math.pi)/4)
    target_offset   = [target_offsetx,target_offsety]
    length          = [lengthx,lengthy]
    height1         = [height1x,height1y]
    height2         = [height2x,height2y]
    rotationlist    = [rotation]
    trgt_lngth_hght1_hght2 = [target_offset,length,height1,height2,rotationlist]
    return trgt_lngth_hght1_hght2

def remove_both_duplicates(perimetre_coords):
    n = 0
    while (len(perimetre_coords) > n):
        m = 0
        while (len(perimetre_coords) > m):
            if (n == m):
                m = n + 1
            if (m == len(perimetre_coords)):
                break
            if (perimetre_coords[n] == perimetre_coords[m]):
                perimetre_coords.pop(n)
                perimetre_coords.pop(m-1)
            m = m + 1
        n = n + 1
    return perimetre_coords

def remove_one_duplicates(coords2):
    coords1 = []
    for item in coords2:
        if item not in coords1:
            coords1.append(item)
    return coords1

def rotation_trig(perimetre_coords,n,target_offset,length,height1,height2,rotation,new_walls):
    rotation_list = [[],[],[],[]]

    if (new_walls == True):
        a = 3
        b = 2
        c = 1
        d = 0
    if (new_walls == False):
        a = 0
        b = 1
        c = 2
        d = 3

    #x' = x*cos(θ)  +  y*sin(θ)
    #y' = y*cos(θ)  -  x*sin(θ)

    rotation_list[a].append((perimetre_coords[n])[0]+(((target_offset[0])*math.cos(-(rotation))) + ((target_offset[1])*math.sin(-(rotation)))))
    rotation_list[a].append((perimetre_coords[n])[1]+(((target_offset[1])*math.cos(-(rotation))) - ((target_offset[0])*math.sin(-(rotation)))))

    rotation_list[b].append((perimetre_coords[n])[0]+(((target_offset[0]+height1[0])*math.cos(-(rotation))) + ((target_offset[1]+height1[1])*math.sin(-(rotation)))))
    rotation_list[b].append((perimetre_coords[n])[1]+(((target_offset[1]+height1[1])*math.cos(-(rotation))) - ((target_offset[0]+height1[0])*math.sin(-(rotation)))))

    rotation_list[c].append((perimetre_coords[n])[0]+(((target_offset[0]+height2[0]+length[0])*math.cos(-(rotation))) + ((target_offset[1]+height2[1]+length[1])*math.sin(-(rotation)))))
    rotation_list[c].append((perimetre_coords[n])[1]+(((target_offset[1]+height2[1]+length[1])*math.cos(-(rotation))) - ((target_offset[0]+height2[0]+length[0])*math.sin(-(rotation)))))

    rotation_list[d].append((perimetre_coords[n])[0]+(((target_offset[0]+length[0])*math.cos(-(rotation))) + ((target_offset[1]+length[1])*math.sin(-(rotation)))))
    rotation_list[d].append((perimetre_coords[n])[1]+(((target_offset[1]+length[1])*math.cos(-(rotation))) - ((target_offset[0]+length[0])*math.sin(-(rotation)))))

    feature_Coords = remove_one_duplicates(rotation_list)
    return feature_Coords

def adding_feature_coords(perimetre_coords,n,target_offset,feature,first_free,new_walls):
    direction = direction_check(perimetre_coords,n)
    direction_words(direction)
    
    rotation_state = direction[0]
    rotation = direction[1]
    trgt_lngth_hght1_hght2 = axis_variables_setter(rotation_state,target_offset,feature,first_free,rotation)
    target_offset   = trgt_lngth_hght1_hght2[0]
    length          = trgt_lngth_hght1_hght2[1]
    height1         = trgt_lngth_hght1_hght2[2]
    height2         = trgt_lngth_hght1_hght2[3]
    rotation        = (trgt_lngth_hght1_hght2[4])[0]

    feature_Coords = rotation_trig(perimetre_coords,n,target_offset,length,height1,height2,rotation,new_walls)

    m = 0
    while (len(feature_Coords) > m):
        xy1 = feature_Coords[m]
        perimetre_coords.insert(n+1,xy1)
        n = n + 1
        m = m + 1
    if (new_walls == False):
        perimetre_coords = remove_both_duplicates(perimetre_coords)
    if (new_walls == True):
        perimetre_coords = remove_one_duplicates(perimetre_coords)
    return perimetre_coords

def rounding_outputs(coords):
    n = 0
    while (len(coords) > n):
        (coords[n])[0] = round((coords[n])[0],5)
        (coords[n])[1] = round((coords[n])[1],5)
        n = n + 1
    return coords

def splitting_coords(perimetre_coords):
    n = 0
    x_list = []
    y_list = []
    while (2 > n):
        m = 0
        while (len(perimetre_coords) > m):
            if (n == 0):
                x_list.append((perimetre_coords[m])[n])
            if (n == 1):
                y_list.append((perimetre_coords[m])[n])
            m = m + 1
        n = n + 1
    lists = [x_list,y_list]
    return lists

def finding_area(lists):
    print("how do i do this")
    n = 0
    sum = 0
    x_list = lists[0]
    y_list = lists[1]

    while (len(x_list) > n):
        if (len(x_list)-1 > n):
            m = n + 1
        if (n == len(x_list)-1):
            m = 0
        sum = sum + ((x_list[n]*y_list[m])-((y_list[n]*x_list[m])))
        n = n + 1

    area = abs(sum/2)
    return area

def is_in_polygon(perimetre_coords,point):
    # A Python3 program to check if a given point 
    # lies inside a given polygon
    # Refer https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
    # for explanation of functions onSegment(),
    # orientation() and doIntersect() 
    
    # Define Infinite (Using INT_MAX 
    # caused overflow problems)
    INT_MAX = 40075017
    
    # Given three collinear points p, q, r, 
    # the function checks if point q lies
    # on line segment 'pr'
    def onSegment(p:tuple, q:tuple, r:tuple) -> bool:
        
        if ((q[0] <= max(p[0], r[0])) &
            (q[0] >= min(p[0], r[0])) &
            (q[1] <= max(p[1], r[1])) &
            (q[1] >= min(p[1], r[1]))):
            return True
            
        return False
    
    # To find orientation of ordered triplet (p, q, r).
    # The function returns following values
    # 0 --> p, q and r are collinear
    # 1 --> Clockwise
    # 2 --> Counterclockwise
    def orientation(p:tuple, q:tuple, r:tuple) -> int:
        
        val = (((q[1] - p[1]) *
                (r[0] - q[0])) -
            ((q[0] - p[0]) *
                (r[1] - q[1])))
                
        if val == 0:
            return 0
        if val > 0:
            return 1 # Collinear
        else:
            return 2 # Clock or counterclock
    
    def doIntersect(p1, q1, p2, q2):
        
        # Find the four orientations needed for 
        # general and special cases
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)
    
        # General case
        if (o1 != o2) and (o3 != o4):
            return True
        
        # Special Cases
        # p1, q1 and p2 are collinear and
        # p2 lies on segment p1q1
        if (o1 == 0) and (onSegment(p1, p2, q1)):
            return True
    
        # p1, q1 and p2 are collinear and
        # q2 lies on segment p1q1
        if (o2 == 0) and (onSegment(p1, q2, q1)):
            return True
    
        # p2, q2 and p1 are collinear and
        # p1 lies on segment p2q2
        if (o3 == 0) and (onSegment(p2, p1, q2)):
            return True
    
        # p2, q2 and q1 are collinear and
        # q1 lies on segment p2q2
        if (o4 == 0) and (onSegment(p2, q1, q2)):
            return True
    
        return False
    
    # Returns true if the point p lies 
    # inside the polygon[] with n vertices
    def is_inside_polygon(points:list, p:tuple) -> bool:
        
        n = len(points)
        
        # There must be at least 3 vertices
        # in polygon
        if n < 3:
            return False
            
        # Create a point for line segment
        # from p to infinite
        extreme = (INT_MAX, p[1])
        count = i = 0
        
        while True:
            next = (i + 1) % n
            
            # Check if the line segment from 'p' to 
            # 'extreme' intersects with the line 
            # segment from 'polygon[i]' to 'polygon[next]'
            if (doIntersect(points[i],
                            points[next],
                            p, extreme)):
                                
                # If the point 'p' is collinear with line 
                # segment 'i-next', then check if it lies 
                # on segment. If it lies, return true, otherwise false
                if orientation(points[i], p,
                            points[next]) == 0:
                    return onSegment(points[i], p,
                                    points[next])
                                    
                count += 1
                
            i = next
            
            if (i == 0):
                break
            
        # Return true if count is odd, false otherwise
        return (count % 2 == 1)
    
    # Driver code
    if __name__ == '__main__':
        ###################################################################################### this is where to add the perimetre chords and points
        polygon1 = perimetre_coords
        
        p = point
        if (is_inside_polygon(points = polygon1, p = p)):
            print ('Yes')
        else:
            print ('No')
        
        """p = (5, 5)
        if (is_inside_polygon(points = polygon1, p = p)):
            print ('Yes')
        else:
            print ('No')
    
        polygon2 = [ (0, 0), (5, 0), (5, 5), (3, 3) ]
        
        p = (3, 3)
        if (is_inside_polygon(points = polygon2, p = p)):
            print ('Yes')
        else:
            print ('No')
        
        p = (5, 1)
        if (is_inside_polygon(points = polygon2, p = p)):
            print ('Yes')
        else:
            print ('No')
        
        p = (8, 1)
        if (is_inside_polygon(points = polygon2, p = p)):
            print ('Yes')
        else:
            print ('No')
        
        polygon3 = [ (0, 0), (10, 0), (10, 10), (0, 10) ]
        
        p = (-1, 10)
        if (is_inside_polygon(points = polygon3, p = p)):
            print ('Yes')
        else:
            print ('No')"""

def extra_data_for_js(perimetre_coords,outer_perimetre_coords):
    lists = splitting_coords(outer_perimetre_coords)
    x_list = copy(lists[0])
    y_list = copy(lists[1])
    x_list.sort()
    y_list.sort()
    max_lengths = []
    max_lengths.append(math.dist([x_list[0]],[x_list[len(x_list)-1]]))
    max_lengths.append(math.dist([y_list[0]],[y_list[len(y_list)-1]]))

    area = finding_area(lists)
    print("area: ", area)

    class data_for_js:
        perimetre = 'this is where the perimetre should be'
        outer_perim = 'this is where the external perimetre should be'
        xy_max_lens = 'this is where the max lengths should be'
            
    #create object
    some_data_for_js = data_for_js()
    some_data_for_js.perimetre = copy(perimetre_coords)
    some_data_for_js.outer_perim = copy(outer_perimetre_coords)
    some_data_for_js.xy_max_lens = copy(max_lengths)

    #convert to JSON string
    js_data = json.dumps(some_data_for_js.__dict__)
    js_prmtr_crds = [js_data,perimetre_coords]
    #print json string
    print(js_prmtr_crds)

    return js_prmtr_crds

def feature_coords(feature,perimetre_coords):
    #feature = [typelist, subtype, subsubtype, offset, length, height1, height2, inward, inneroffset, name, leadingto]
    
    if (len(perimetre_coords) == 1):
        n = 0
        target_offset = 0
        first_free = True
        new_walls = True
        perimetre_coords = adding_feature_coords(perimetre_coords,n,target_offset,feature,first_free,new_walls)
        return perimetre_coords

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
            new_walls = False
            perimetre_coords = adding_feature_coords(perimetre_coords,n,target_offset,feature,first_free,new_walls)
        return perimetre_coords

def wall_thickness(year_built):
    if (year_built <= 1700):
        exterior_wall = 1.50
        interior_wall = 1.00
    if (1700 < year_built <= 1850):
        exterior_wall = 0.80
        interior_wall = 0.50
    if (1850 < year_built <= 1990):
        exterior_wall = 0.50
        interior_wall = 0.30
    if (1990 < year_built):
        exterior_wall = 0.30
        interior_wall = 0.20
    wall_size = [exterior_wall,interior_wall]
    return wall_size

def outer_offset_coords(angle,coord_pair,wall_size):
    n = 0
    while (len(coord_pair) > n):
        coords = coord_pair[n]
        if (angle[0] == 0):
            x = (coords[0])
            y = (coords[1]) - (wall_size[0])

        if (angle[0] == 1):
            x = (coords[0]) + (wall_size[0]/math.sin((math.pi/2)-(angle[1])))
            y = (coords[1]) - (wall_size[0]/math.cos((math.pi/2)-(angle[1])))
            
        if (angle[0] == 2):
            x = (coords[0]) + (wall_size[0])
            y = (coords[1])
            
        if (angle[0] == 3):
            x = (coords[0]) + (wall_size[0])/math.sin((math.pi/2)-(angle[1]))
            y = (coords[1]) + (wall_size[0])/math.cos((math.pi/2)-(angle[1]))
            
        if (angle[0] == 4):
            x = (coords[0])
            y = (coords[1]) + (wall_size[0])
            
        if (angle[0] == 5):
            x = (coords[0]) - (wall_size[0])/math.sin((math.pi/2)-(angle[1]))
            y = (coords[1]) + (wall_size[0])/math.cos((math.pi/2)-(angle[1]))
            
        if (angle[0] == 6):
            x = (coords[0]) - (wall_size[0])
            y = (coords[1])
            
        if (angle[0] == 7):
            x = (coords[0]) - (wall_size[0])/math.sin((math.pi/2)-(angle[1]))
            y = (coords[1]) - (wall_size[0])/math.sin((math.pi/2)-(angle[1]))
        
        coord_pair[n] = [x,y]
        n = n + 1
    
    return coord_pair

def outer_perimetre(perimetre_coords,wall_size):
    n = 0
    outer_perimetre_coords = []
    while (len(perimetre_coords) > n):

        if (len(perimetre_coords) > n):
            m = n+1
            v = m+1
        if (len(perimetre_coords)-1 == m):
            m = n+1
            v = 0
        if (len(perimetre_coords) == m):
            m = 0
            v = m+1
        #if (len(perimetre_coords) == n):
        #    break
            
        
        a = perimetre_coords[n]
        b = perimetre_coords[m]
        c = perimetre_coords[m]
        d = perimetre_coords[v]

        angle = direction_check(perimetre_coords,n)
        coord_pair = [a,b]
        coord_pair = outer_offset_coords(angle,coord_pair,wall_size)
        a = coord_pair[0]
        b = coord_pair[1]

        angle = direction_check(perimetre_coords,n+1)
        coord_pair = [c,d]
        coord_pair = outer_offset_coords(angle,coord_pair,wall_size)
        c = coord_pair[0]
        d = coord_pair[1]


        t = ((((a[0]-c[0])*(c[1]-d[1]))-((a[1]-c[1])*(c[0]-d[0])))/(((a[0]-b[0])*(c[1]-d[1]))-((a[1]-b[1])*(c[0]-d[0]))))
        x = (a[0] + t*(b[0]-a[0]))
        y = (a[1] + t*(b[1]-a[1]))

        #u = ((((a[0]-c[0])*(a[1]-b[1]))-((a[1]-c[1])*(a[0]-b[0])))/(((a[0]-b[0])*(c[1]-d[1]))-((a[1]-b[1])*(c[0]-d[0]))))
        #x = (c[0] + u*(d[0]-c[0]))
        #y = (c[1] + u*(d[1]-c[1]))

        outer_perimetre_coords.append([x,y])
        n = n + 1
    return outer_perimetre_coords

def error_check(perimetre_coords):
    def intersection_error(perimetre_coords):
        class Point:
            def __init__(self, x, y):
                    self.x = x
                    self.y = y
        
        # Given three collinear points p, q, r, the function checks if 
        # point q lies on line segment 'pr' 
        def onSegment(p, q, r):
            if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
                (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
                return True
            return False
        
        def orientation(p, q, r):
            # to find the orientation of an ordered triplet (p,q,r)
            # function returns the following values:
            # 0 : Collinear points
            # 1 : Clockwise points
            # 2 : Counterclockwise
            
            # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/ 
            # for details of below formula. 
            
            val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
            if (val > 0):
                
                # Clockwise orientation
                return 1
            elif (val < 0):
                
                # Counterclockwise orientation
                return 2
            else:
                
                # Collinear orientation
                return 0
        
        # The main function that returns true if 
        # the line segment 'p1q1' and 'p2q2' intersect.
        def doIntersect(p1,q1,p2,q2):
            
            # Find the 4 orientations required for 
            # the general and special cases
            o1 = orientation(p1, q1, p2)
            o2 = orientation(p1, q1, q2)
            o3 = orientation(p2, q2, p1)
            o4 = orientation(p2, q2, q1)
        
            # General case
            if ((o1 != o2) and (o3 != o4)):
                return True
        
            # Special Cases
        
            # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
            if ((o1 == 0) and onSegment(p1, p2, q1)):
                return True
        
            # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
            if ((o2 == 0) and onSegment(p1, q2, q1)):
                return True
        
            # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
            if ((o3 == 0) and onSegment(p2, p1, q2)):
                return True
        
            # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
            if ((o4 == 0) and onSegment(p2, q1, q2)):
                return True
        
            # If none of the cases
            return False
        
        # Driver program to test above functions:
        
        n = 0
        while (len(perimetre_coords) > n):
            m = 0
            while (len(perimetre_coords) > m):
                if (n == m):
                    m = n + 1
                if (m == len(perimetre_coords)):
                    break
                if ((len(perimetre_coords) > n) and (len(perimetre_coords) > m)):
                    p1 = perimetre_coords[n]
                    q1 = perimetre_coords[n+1]
                    p2 = perimetre_coords[m]
                    q2 = perimetre_coords[m+1]
                    if doIntersect(p1, q1, p2, q2):
                       return True
                    else:
                        return False
                m = m + 1
            n = n + 1   
        """p1 = Point(10, 0)
        q1 = Point(0, 10)
        p2 = Point(0, 0)
        q2 = Point(10,10)
        
        if doIntersect(p1, q1, p2, q2):
            print("Yes")
        else:
            print("No")
        
        p1 = Point(-5,-5)
        q1 = Point(0, 0)
        p2 = Point(1, 1)
        q2 = Point(10, 10)
        
        if doIntersect(p1, q1, p2, q2):
            print("Yes")
        else:
            print("No")
    #if (intersection_error(perimetre_coords) == True):
    #    print("INTERSECTION ERROR STOP!!!!!!!!!!!!!!!!!!!!!!!")
    #else:
    #    print("no intersection error")"""

def start_the_programe(box,features,year_built):
    walls_feature=initial_perim(box[0],box[1])

    features.insert(0,walls_feature)

    perimetre_coords = [[0,0]]

    n = 0
    while (n < len(features)):
        if ((features[n])[0] == 0):
            print("the feature is a triangle or rectangle thing")
            perimetre_coords = feature_coords(features[n],perimetre_coords)
            perimetre_coords = rounding_outputs(perimetre_coords)
            error_check(perimetre_coords)
        print (perimetre_coords)
        print("room perimetre: ", perimetre_length(perimetre_coords,0)[0])

        n = n + 1
    

    wall_size = wall_thickness(year_built)
    outer_perimetre_coords = outer_perimetre(perimetre_coords,wall_size)
    outer_perimetre_coords = rounding_outputs(outer_perimetre_coords)

    point = [200,5]
    print(perimetre_coords)
    is_in_polygon(perimetre_coords,point)


    js_prmtr_crds = extra_data_for_js(perimetre_coords,outer_perimetre_coords)
    js_data = js_prmtr_crds[0]
    perimetre_coords = js_prmtr_crds[1]





    return js_data
    #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")








#print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")



#the thing that starts it on its own
"""
year_built = 2022
box = [20,20]
features = [[0, 0, 0, 7, 3, 0, 4, 0, 0, "triangle feature thing1", ""]
           ,[0, 0, 0, 8, 1, 1, 1, 0, 0, "triangle feature thing2", ""]]
#features = [[0, 0, 0, 15, 5, 0, 5, 0, 0, "triangle feature thing1", ""]]

room_output = start_the_programe(box,features,year_built)"""


    

#features = [[0, 0, 0, 3, 2, 3, 1, 0, 0, "triangle feature thing1", ""]]
#features = [[0, 0, 0, 3, 2, 3, 3, 0, 0, "triangle feature thing1", ""]
#           ,[0, 0, 0, 7, 1, 1, 1, 0, 0, "triangle feature thing2", ""]]











#feature = [typelist, subtype, subsubtype, offset, length, height1, height2, inward, inneroffset, name, leadingto]


