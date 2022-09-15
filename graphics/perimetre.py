#
# 
# perimetre format
# [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
#
#
# feature format
# [typelist, subtype, offset, length, height1, height2, inward, side, inneroffset, name, leadingto]
#
#
# preset wall list format
# [[thickness1, type1], [thickness2, type2], [thickness3, type3]]
#
#
# feature types
# 1) walls
#     a) rectangles/triangles
#     b) bays
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
# 4) radiator
#
# 
# things that can overlap...
# 1) windows    /   walls,  door,       radiators
# 2) doors      /   walls,  windows
# 3) radiators  /   walls,  windows



from __future__ import division
from copy import copy
import math
import json
from re import U
import random

def perimetre_length(coords,upto_point):
    if (upto_point <= 0):
        array_length = len(coords)
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
        distance = round(math.dist((coords[n]), (coords[m+1])),5)
        (length[1]).append(distance)
        length[0] = length[0] + (distance)
        print("room wall: ", n+1, " wall length: ", (distance))
        n = n + 1
    return length

def direction_check(coords,n):
    # for all but the last coordinate
    if (len(coords)-1 > n):
        m = n+1
    # linking the last coordinate to the first coordinate
    if ((n == len(coords)-1) or (len(coords) == 1)):
        m = 0
    if (n == len(coords)):
        n = 0
        m = n + 1
    
    #special case where x and y is the same
    if (((coords[n])[0] == (coords[m])[0]) and ((coords[n])[1] == (coords[m])[1])):
        direction = [0,((0*math.pi)/2)]
        return direction


    #print("the x is different and y is same")
    if (((coords[n])[0] != (coords[m])[0]) and ((coords[n])[1] == (coords[m])[1])):
        # horizontal
        # right
        if ((coords[n])[0] < (coords[m])[0]):
            direction = [0,((0*math.pi)/2)]
            return direction
        # left
        if ((coords[n])[0] > (coords[m])[0]):
            direction = [4,((2*math.pi)/2)]
            return direction
    #print("the y is different and x is same")
    if (((coords[n])[1] != (coords[m])[1]) and ((coords[n])[0] == (coords[m])[0])):
        # veritcal
        # down
        if ((coords[n])[1] < (coords[m])[1]):
            direction = [2,((1*math.pi)/2)]
            return direction
        # up
        if ((coords[n])[1] > (coords[m])[1]):
            direction = [6,((3*math.pi)/2)]
            return direction
    #print("the x and y is different")
    if (((coords[n])[0] != (coords[m])[0]) and ((coords[n])[1] != (coords[m])[1])):
        # diagonal
        # right,down
        if (((coords[n])[0] < (coords[m])[0]) and ((coords[n])[1] < (coords[m])[1])):
            angle = math.atan(math.dist([(coords[n])[1]], [(coords[m])[1]])/math.dist([(coords[n])[0]], [(coords[m])[0]]))
            direction = [1,angle]
            return direction
        # right,up
        if (((coords[n])[0] < (coords[m])[0]) and ((coords[n])[1] > (coords[m])[1])):
            angle = math.atan((math.dist([(coords[n])[1]],[(coords[m])[1]]))/(math.dist([(coords[n])[0]],[(coords[m])[0]])))
            direction = [7,angle]
            return direction
        # left,down
        if (((coords[n])[0] > (coords[m])[0]) and ((coords[n])[1] < (coords[m])[1])):
            angle = math.atan((math.dist([(coords[n])[1]],[(coords[m])[1]]))/(math.dist([(coords[n])[0]],[(coords[m])[0]])))
            direction = [3,angle]
            return direction
        # left,up
        if (((coords[n])[0] > (coords[m])[0]) and ((coords[n])[1] > (coords[m])[1])):
            angle = math.atan((math.dist([(coords[n])[1]],[(coords[m])[1]]))/(math.dist([(coords[n])[0]],[(coords[m])[0]])))
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

def rotation_for_segments(rotation_state,rotation):
    if (rotation_state == 1):
        rotation = rotation + ((0*math.pi)/2)
    if (rotation_state == 3):
        rotation = rotation + ((1*math.pi)/2)
    if (rotation_state == 5):
        rotation = rotation + ((2*math.pi)/2)
    if (rotation_state == 7):
        rotation = rotation + ((3*math.pi)/2)

    return rotation

def remove_both_duplicates(coords):
    n = 0
    while (len(coords) > n):
        m = 0
        while (len(coords) > m):
            if (n == m):
                m = n + 1
            if (m == len(coords)):
                break
            if (coords[n] == coords[m]):
                coords.pop(n)
                coords.pop(m-1)
            m = m + 1
        n = n + 1
    return coords

def remove_one_duplicates(coords2):
    coords1 = []
    for item in coords2:
        if item not in coords1:
            coords1.append(item)
    return coords1

def rounding_outputs(coords):
    n = 0
    while (len(coords) > n):
        (coords[n])[0] = round((coords[n])[0],5)
        (coords[n])[1] = round((coords[n])[1],5)
        n = n + 1
    return coords

def gathering_specs():
    with open("room.txt", "r") as fp:
        # read all lines in a list
        items = json.loads("".join(("".join(fp.readlines())).split()))
        
    info_stuff =            items["info"]
    year_built =            (info_stuff[0])["YearBuilt"]
    box =                   [(((info_stuff[1])["BoxSize"])[0])["width"],(((info_stuff[1])["BoxSize"])[1])["height"]]
    preset_wall_list = (info_stuff[2])["PresetWalls"]
    featuresdict =          (info_stuff[3])["Features"]

    features = []

    for featuredict in featuresdict:

        feature = []
        
        feature.append(((featuredict["feature"])[0])["typelist"])
        feature.append(((featuredict["feature"])[1])["subtype"])
        feature.append(((featuredict["feature"])[2])["offset"])
        feature.append(((featuredict["feature"])[3])["length"])
        feature.append(((featuredict["feature"])[4])["height1"])
        feature.append(((featuredict["feature"])[5])["height2"])
        feature.append(((featuredict["feature"])[6])["inward"])
        feature.append(((featuredict["feature"])[7])["side"])
        feature.append(((featuredict["feature"])[8])["inneroffset"])
        feature.append(((featuredict["feature"])[9])["name"])
        feature.append(((featuredict["feature"])[10])["leadingto"])

        features.append(feature)
    
    def quicksort_features(features):
        # Python program for implementation of Quicksort Sort
        # This implementation utilizes pivot as the last element in the nums list
        # It has a pointer to keep track of the elements smaller than the pivot
        # At the very end of partition() function, the pointer is swapped with the pivot
        # to come up with a "sorted" nums relative to the pivot
        def partition(l, r, nums):
            # Last element will be the pivot and the first element the pointer
            pivot, ptr = nums[r], l
            for i in range(l, r):
                if nums[i] <= pivot:
                    # Swapping values smaller than the pivot to the front
                    nums[i], nums[ptr] = nums[ptr], nums[i]
                    ptr += 1
            # Finally swapping the last element with the pointer indexed number
            nums[ptr], nums[r] = nums[r], nums[ptr]
            return ptr
        
        # With quicksort() function, we will be utilizing the above code to obtain the pointer
        # at which the left values are all smaller than the number at pointer index and vice versa
        # for the right values.
        
        
        def quicksort(l, r, nums):
            if len(nums) == 1:  # Terminating Condition for recursion. VERY IMPORTANT!
                return nums
            if l < r:
                pi = partition(l, r, nums)
                quicksort(l, pi-1, nums)  # Recursively sorting the left values
                quicksort(pi+1, r, nums)  # Recursively sorting the right values
            return nums
        
        
        example = [4, 5, 1, 2, 3]
        result = [1, 2, 3, 4, 5]
        print(quicksort(0, len(example)-1, example))
        
        example = [2, 5, 6, 1, 4, 6, 2, 4, 7, 8]
        result = [1, 2, 2, 4, 4, 5, 6, 6, 7, 8]

    features = quicksort_features(features)


    file_data = [year_built,box,preset_wall_list,features]

    return file_data




# store coordinates in segments instead of points???
# non wall features need to not be used in calculation of outer perim




def gathering_data_for_js(perimetre_coords,outer_perimetre_coords):

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

    def segmenting(coords):
        segments = []
        n = 0
        while (len(coords) > n):

            if (len(coords)-1 > n):
                m = n + 1
            if (len(coords)-1 == n):
                m = 0
        
            segments.append([coords[n],coords[m]])

            n = n + 1

        return segments

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

        perimetre_segments = segmenting(perimetre_coords)
        out_perim_segments = segmenting(outer_perimetre_coords)

        class data_for_js:
            perimetre = 'this is where the perimetre should be'
            outer_perim = 'this is where the external perimetre should be'
            xy_max_lens = 'this is where the max lengths should be'
            perimetre_segments = 'this is where the segments of the perimetre go'
            outer_perim_segments = 'this is where the segments of the external perimetre go'
            #the_wall_size = 'this is where the thickness of the wall should be'
                
        #create object
        some_data_for_js = data_for_js()
        some_data_for_js.perimetre = copy(perimetre_coords)
        some_data_for_js.outer_perim = copy(outer_perimetre_coords)
        some_data_for_js.xy_max_lens = copy(max_lengths)
        some_data_for_js.perimetre_segments = copy(perimetre_segments)
        some_data_for_js.outer_perim_segments = copy(out_perim_segments)
        #some_data_for_js.the_wall_size = copy(wall_size)

        #convert to JSON string
        js_data = json.dumps(some_data_for_js.__dict__)
        js_prmtr_crds = [js_data,perimetre_coords]
        #print json string
        print(js_prmtr_crds)

        return js_prmtr_crds

    #js_prmtr_crds = extra_data_for_js(perimetre_coords,outer_perimetre_coords)
    #return js_prmtr_crds
    return extra_data_for_js(perimetre_coords,outer_perimetre_coords)



def adding_outer_perimetre(year_built,preset_wall_type_list,perimetre_coords):

    def wall_thickness(year_built,preset_wall_type_list,perimetre_coords):
        fixed = []*len(perimetre_coords)
        if (len(preset_wall_type_list) > 0):
            print()
        if (len(preset_wall_type_list) <= 0):
            print()
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
                x = (coords[0]) + ((wall_size[0])*(math.cos((math.pi/2)-angle[1])))
                y = (coords[1]) - ((wall_size[0])*(math.sin((math.pi/2)-angle[1])))
                
            if (angle[0] == 2):
                x = (coords[0]) + (wall_size[0])
                y = (coords[1])
                
            if (angle[0] == 3):
                x = (coords[0]) + ((wall_size[0])*(math.cos((math.pi/2)-angle[1])))
                y = (coords[1]) + ((wall_size[0])*(math.sin((math.pi/2)-angle[1])))
                
            if (angle[0] == 4):
                x = (coords[0])
                y = (coords[1]) + (wall_size[0])
                
            if (angle[0] == 5):
                x = (coords[0]) - ((wall_size[0])*(math.cos((math.pi/2)-angle[1])))
                y = (coords[1]) + ((wall_size[0])*(math.sin((math.pi/2)-angle[1])))
                
            if (angle[0] == 6):
                x = (coords[0]) - (wall_size[0])
                y = (coords[1])
                
            if (angle[0] == 7):
                x = (coords[0]) - ((wall_size[0])*(math.cos((math.pi/2)-angle[1])))
                y = (coords[1]) - ((wall_size[0])*(math.sin((math.pi/2)-angle[1])))
            
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


            t = ((((a[0]-c[0])*(c[1]-d[1]))-((a[1]-c[1])*(c[0]-d[0])))
                /(((a[0]-b[0])*(c[1]-d[1]))-((a[1]-b[1])*(c[0]-d[0]))))
            x = (a[0] + t*(b[0]-a[0]))
            y = (a[1] + t*(b[1]-a[1]))

            #u = ((((a[0]-c[0])*(a[1]-b[1]))-((a[1]-c[1])*(a[0]-b[0])))
            #    /(((a[0]-b[0])*(c[1]-d[1]))-((a[1]-b[1])*(c[0]-d[0]))))
            #x = (c[0] + u*(d[0]-c[0]))
            #y = (c[1] + u*(d[1]-c[1]))

            outer_perimetre_coords.append([x,y])
            n = n + 1
        
        outer_perimetre_coords.insert(0,(outer_perimetre_coords[len(outer_perimetre_coords)-1]))
        outer_perimetre_coords.pop(len(outer_perimetre_coords)-1)
        
        return outer_perimetre_coords
    
    # wall_size = wall_thickness(year_built,preset_wall_type_list,perimetre_coords)
    #outer_perimetre_coords = outer_perimetre(perimetre_coords,wall_size)
    return outer_perimetre(perimetre_coords,wall_thickness(year_built,preset_wall_type_list,perimetre_coords))



def adding_window_feature(fitting,preset_wall_type_list):

    def window_rotation_trig(perimetre_coords,n,target_offset,length,rotation):
        rotation_list = [[],[]]

        a = 0
        b = 1

            
        #x' = x*cos(θ)  +  y*sin(θ)
        #y' = y*cos(θ)  -  x*sin(θ)

        rotation_list[a].append((perimetre_coords[n])[0]+(((target_offset)*(round(math.cos(-(rotation)),10))) + ((0)            *math.sin(-(rotation)))))
        rotation_list[a].append((perimetre_coords[n])[1]+(((0)            *(round(math.cos(-(rotation)),10))) - ((target_offset)*math.sin(-(rotation)))))

        rotation_list[b].append((perimetre_coords[n])[0]+(((target_offset+length)*(round(math.cos(-(rotation)),10))) + ((0)                   *math.sin(-(rotation)))))
        rotation_list[b].append((perimetre_coords[n])[1]+(((0)                   *(round(math.cos(-(rotation)),10))) - ((target_offset+length)*math.sin(-(rotation)))))

        """
        rotation_list[a].append((perimetre_coords[n])[0]+(((target_offset[0])*(round(math.cos(-(rotation)),10))) + ((target_offset[1])*math.sin(-(rotation)))))
        rotation_list[a].append((perimetre_coords[n])[1]+(((target_offset[1])*(round(math.cos(-(rotation)),10))) - ((target_offset[0])*math.sin(-(rotation)))))

        rotation_list[b].append((perimetre_coords[n])[0]+(((target_offset[0]+length[0])*(round(math.cos(-(rotation)),10))) + ((target_offset[1]+length[1])*math.sin(-(rotation)))))
        rotation_list[b].append((perimetre_coords[n])[1]+(((target_offset[1]+length[1])*(round(math.cos(-(rotation)),10))) - ((target_offset[0]+length[0])*math.sin(-(rotation)))))"""
        return rotation_list

    def adding_window_feature_coords(perimetre_coords,n,target_offset,feature,preset_wall_type_list):
        direction = direction_check(perimetre_coords,n)
        direction_words(direction)
        
        rotation_state = direction[0]
        rotation = direction[1]
        rotation = rotation_for_segments(rotation_state,rotation)

        length = feature[3]
        
        feature_Coords = window_rotation_trig(perimetre_coords,n,target_offset,length,rotation)

        feature_Coords = rounding_outputs(feature_Coords)
        
        feature_Coords = remove_one_duplicates(feature_Coords)


        if (feature_Coords[0] in perimetre_coords):
            preset_wall_type_list.insert(n,1)
        if (feature_Coords[1] in perimetre_coords):
            preset_wall_type_list.insert(n+1,1)
        if ((feature_Coords[0] or feature_Coords[1]) not in perimetre_coords):
            preset_wall_type_list.insert(n+1,0)
            preset_wall_type_list.insert(n+1,1)

        m = 0
        while (len(feature_Coords) > m):
            xy = feature_Coords[m]
            perimetre_coords.insert(n+1,xy)
            n = n + 1
            m = m + 1


        perimetre_coords = remove_one_duplicates(perimetre_coords)





        perim_wall_prst = [perimetre_coords,preset_wall_type_list]
        return perim_wall_prst
    
    # fitting = [perimetre_coords,n,target_offset,feature,first_free,new_walls]
    # perim_wall_prst = adding_window_feature_coords(fitting[0],fitting[1],fitting[2],fitting[3],fitting[4],fitting[5],preset_wall_type_list)
    return adding_window_feature_coords(fitting[0],fitting[1],fitting[2],fitting[3],preset_wall_type_list)


def adding_wall_feature(fitting,preset_wall_type_list):

    def wall_rotation_trig(perimetre_coords,n,target_offset,length,height1,height2,rotation,new_walls):
        rotation_list = [[],[],[],[]]

        if (new_walls == True):
            p = -1
            a = 3
            b = 2
            c = 1
            d = 0
        if (new_walls == False):
            p = -1
            a = 0
            b = 1
            c = 2
            d = 3
            
        #x' = x*cos(θ)  +  y*sin(θ)
        #y' = y*cos(θ)  -  x*sin(θ)

        rotation_list[a].append((perimetre_coords[n])[0]+(((target_offset)*(round(math.cos(-(rotation)),10))) + ((0)            *math.sin(-(rotation)))))
        rotation_list[a].append((perimetre_coords[n])[1]+(((0)            *(round(math.cos(-(rotation)),10))) - ((target_offset)*math.sin(-(rotation)))))

        rotation_list[b].append((perimetre_coords[n])[0]+(((target_offset)*(round(math.cos(-(rotation)),10))) + (((-height1)*p) *math.sin(-(rotation)))))
        rotation_list[b].append((perimetre_coords[n])[1]+((((-height1)*p) *(round(math.cos(-(rotation)),10))) - ((target_offset)*math.sin(-(rotation)))))

        rotation_list[c].append((perimetre_coords[n])[0]+(((target_offset+length)*(round(math.cos(-(rotation)),10))) + (((-height2)*p)        *math.sin(-(rotation)))))
        rotation_list[c].append((perimetre_coords[n])[1]+((((-height2)*p)        *(round(math.cos(-(rotation)),10))) - ((target_offset+length)*math.sin(-(rotation)))))

        rotation_list[d].append((perimetre_coords[n])[0]+(((target_offset+length)*(round(math.cos(-(rotation)),10))) + ((0)                   *math.sin(-(rotation)))))
        rotation_list[d].append((perimetre_coords[n])[1]+(((0)                   *(round(math.cos(-(rotation)),10))) - ((target_offset+length)*math.sin(-(rotation)))))

        """
        rotation_list[a].append((perimetre_coords[n])[0]+(((target_offset[0])*(round(math.cos(-(rotation)),10))) + ((target_offset[1])*math.sin(-(rotation)))))
        rotation_list[a].append((perimetre_coords[n])[1]+(((target_offset[1])*(round(math.cos(-(rotation)),10))) - ((target_offset[0])*math.sin(-(rotation)))))

        rotation_list[b].append((perimetre_coords[n])[0]+(((target_offset[0]+height1[0])*(round(math.cos(-(rotation)),10))) + ((target_offset[1]+height1[1])*math.sin(-(rotation)))))
        rotation_list[b].append((perimetre_coords[n])[1]+(((target_offset[1]+height1[1])*(round(math.cos(-(rotation)),10))) - ((target_offset[0]+height1[0])*math.sin(-(rotation)))))

        rotation_list[c].append((perimetre_coords[n])[0]+(((target_offset[0]+height2[0]+length[0])*(round(math.cos(-(rotation)),10))) + ((target_offset[1]+height2[1]+length[1])*math.sin(-(rotation)))))
        rotation_list[c].append((perimetre_coords[n])[1]+(((target_offset[1]+height2[1]+length[1])*(round(math.cos(-(rotation)),10))) - ((target_offset[0]+height2[0]+length[0])*math.sin(-(rotation)))))

        rotation_list[d].append((perimetre_coords[n])[0]+(((target_offset[0]+length[0])*(round(math.cos(-(rotation)),10))) + ((target_offset[1]+length[1])*math.sin(-(rotation)))))
        rotation_list[d].append((perimetre_coords[n])[1]+(((target_offset[1]+length[1])*(round(math.cos(-(rotation)),10))) - ((target_offset[0]+length[0])*math.sin(-(rotation)))))"""
        return rotation_list

    def adding_wall_feature_coords(perimetre_coords,n,target_offset,feature,first_free,new_walls,preset_wall_type_list):
        direction = direction_check(perimetre_coords,n)
        direction_words(direction)
        
        rotation_state = direction[0]
        rotation = direction[1]
        rotation = rotation_for_segments(rotation_state,rotation)

        if (first_free == True):
            target_offset = 0
        length            = feature[3]
        height1           = feature[4]
        height2           = feature[5]

        
        feature_Coords = wall_rotation_trig(perimetre_coords,n,target_offset,length,height1,height2,rotation,new_walls)

        feature_Coords = rounding_outputs(feature_Coords)
        
        feature_Coords = remove_one_duplicates(feature_Coords)

        u = copy(n)

        m = 0
        while (len(feature_Coords) > m):
            xy = feature_Coords[m]
            perimetre_coords.insert(n+1,xy)
            n = n + 1
            m = m + 1

        if (new_walls == False):
            m = 0
            while (len(feature_Coords) > m):
                preset_wall_type_list.insert(u+1,0)
                u = u + 1
                m = m + 1
            perimetre_coords = remove_both_duplicates(perimetre_coords)

        if (new_walls == True):
            preset_wall_type_list = [0,0,0,0]
            perimetre_coords = remove_one_duplicates(perimetre_coords)

        perim_wall_prst = [perimetre_coords,preset_wall_type_list]
        return perim_wall_prst
    
    # fitting = [perimetre_coords,n,target_offset,feature,first_free,new_walls]
    # perim_wall_prst = adding_wall_feature_coords(fitting[0],fitting[1],fitting[2],fitting[3],fitting[4],fitting[5],preset_wall_type_list)
    return adding_wall_feature_coords(fitting[0],fitting[1],fitting[2],fitting[3],fitting[4],fitting[5],preset_wall_type_list)



def does_it_fit(feature,perimetre_coords,preset_wall_type_list):

    def type_check(f_type,w_type):
        # 0 = wall
        # 1 = window
        # 2 = door
        # 3 = radiator
        if (w_type == 0):
            return True
        if ((w_type == 1) and ((f_type == 2) or (f_type == 3))):
            return True
        if ((w_type == 2) and (f_type == 1)):
            return True
        if ((w_type == 3) and (f_type == 1)):
            return True
        else:
            return False

    def fit_check(feature,perimetre_coords,preset_wall_type_list):
        # feature[3] is a real number that represents the length of the feature that may be added.
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
            
            if (feature[3] >= math.dist((perimetre_coords[n]), (perimetre_coords[m+1]))):
                print("the length doesnt fit")
                fits.append(0)
            else:
                type_fit = type_check(feature[0],preset_wall_type_list[n])
                if (type_fit == True):
                    fits.append(1)
                if (type_fit == False):
                    fits.append(0)
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
        target_offset = feature[2]
        walls = []
        n = 0
        if (len(perimetre_coords)-1 > n):
            m = n+1
        if (n == len(perimetre_coords)-1):
            m = 0
        while (target_offset+feature[3] > math.dist(perimetre_coords[n],perimetre_coords[m])):
            target_offset = target_offset - math.dist(perimetre_coords[n],perimetre_coords[m])
            walls.append(0)
            n = n + 1

            if (len(perimetre_coords)-1 > n):
                m = n+1
            if (n == len(perimetre_coords)-1):
                m = 0
        walls.append(1)
        walls_target_offset = [walls,target_offset]
        return walls_target_offset

    def first_free_decider(walls,fits,target_offset):
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
        if (target_offset <= 0):
            first_free = True
        n_first_free = [n,first_free]
        return n_first_free

    def feature_coords(feature,perimetre_coords,preset_wall_type_list):
        # feature = [typelist, subtype, offset, length, height1, height2, inward, side, inneroffset, name, leadingto]
        
        if (len(perimetre_coords) == 1):
            n = 0
            target_offset = 0
            first_free = True
            new_walls = True
            fitting = [perimetre_coords,n,target_offset,feature,first_free,new_walls]
            return fitting

        fits = fit_check(feature,perimetre_coords,preset_wall_type_list)
        n = 0
        sum = 0
        while (n < len(fits)):
            sum = sum + fits[n]
            n = n + 1
        
        if (sum != 0):

            walls_target_offset = offset_length_fit_check(perimetre_coords,feature)
            walls = walls_target_offset[0]
            target_offset = walls_target_offset[1]

            n_first_free = first_free_decider(walls,fits,target_offset)
            n = n_first_free[0]
            first_free = n_first_free[1]

            if (fits[n] == 1):

                print("it can start drawing the feature")
                new_walls = False

                fitting = [perimetre_coords,n,target_offset,feature,first_free,new_walls]
            
            return fitting
        
        else:
            return False

    #fitting = feature_coords(feature,perimetre_coords,preset_wall_type_list)
    return feature_coords(feature,perimetre_coords,preset_wall_type_list)








def start_the_programe():

    file_data = gathering_specs()
    year_built          = file_data[0]
    box                 = file_data[1]
    preset_wall_list    = file_data[2]
    features            = file_data[3]

    walls_feature = [0, 0, 0, box[0], box[1], box[1], 0, 0, 0, "walls", ""]
    features.insert(0,walls_feature)

    perimetre_coords = [[0,0]]
    preset_wall_type_list = []

    for feature in features:
        fitting = does_it_fit(feature,perimetre_coords,preset_wall_type_list)

        if (((feature)[0] == 0) and (fitting != False)):
            print("the feature is a triangle or rectangle thing")
            perim_wall_prst =       adding_wall_feature(fitting,preset_wall_type_list)
            perimetre_coords =      perim_wall_prst[0]
            preset_wall_type_list = perim_wall_prst[1]

        if (((feature)[0] == 1) and (fitting != False)):
            print("the feature is a window")
            perim_wall_prst =       adding_window_feature(fitting,preset_wall_type_list)
            perimetre_coords =      perim_wall_prst[0]
            preset_wall_type_list = perim_wall_prst[1]


        perimetre_coords = rounding_outputs(perimetre_coords)
        print (perimetre_coords)
        print("room perimetre: ", perimetre_length(perimetre_coords,0)[0])
    
    
    outer_perimetre_coords = adding_outer_perimetre(year_built,preset_wall_type_list,perimetre_coords)

    #outer_perimetre_coords = outer_perimetre(perimetre_coords,wall_size)
    outer_perimetre_coords = rounding_outputs(outer_perimetre_coords)


    print(perimetre_coords)
    print(outer_perimetre_coords)

    js_prmtr_crds = gathering_data_for_js(perimetre_coords,outer_perimetre_coords)
    js_data = js_prmtr_crds[0]
    perimetre_coords = js_prmtr_crds[1]





    return js_data
    #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")







# plan!!!
# group together the parts of the code which...
# 1) check if a feature can fit
# 2) places the feature where it needs to be
# 3) sorts out the outer perimetre 
# 4) adds verification 
#
# then i need to...
# 1) rewrite the parts between the functions so it still works
# 2) delete the functions that have been relocated from their old postitions
# 3) put the other functions in one place at the start of the program
# 4) add the idea about the preset_wall_type_list variable identifying wall thickness and wall types accross the entire room
# 5) fix whatever bugs that has caused
# 6) clean up the code generally and add comments
# 7) dont break anything in the previous step
# 8) dont make a mess in any of the previous steps
#
# following this i will need to...
# 1) fix the outer perimeter code
# 2) write the lines intersection verification code in the group
# 3) bug fix whatever doesn’t work
# 4) celebrate its workingness
# 5) break it again with whatever i think of in the process of doing this






print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


#room_output = start_the_programe()



#feature = [typelist, subtype, offset, length, height1, height2, inward, side, inneroffset, name, leadingto]


