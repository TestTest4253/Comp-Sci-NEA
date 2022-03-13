# For the Texture analysis
import numpy as np
import math

# For the Datastore
import os
import pyrebase
import urllib


def local_binary_pattern(image):

    """
    Inputs:
        image {type: Array[r,c]} Greyscale image of the intended image to be calculated

    Outputs:
        FinalArray {type: List[r,c]} Array of the LBP points for each pixel 
    """


    Width, Height = math.ceil((len(image[0]))), math.ceil((len(image)))
    array = image.tolist()
    SingleRow, rows, Row, grids, LocalBinaryImageList, FinalArray = [], [], [], [], [], []

    # Splits photo into 3 long groupings
    for row in range(len(array)):
        for column in range(len(array)):
            SingleRow.append(array[row][column:column + 3])
        SingleRow.append("NEW LINE")
    for x in range(len(SingleRow)):
        if SingleRow[x] == "NEW LINE":
            rows.append(Row)
            Row = []
        else:
            Row.append(SingleRow[x])

    for row in range(len(rows)):
        grids_row = []
        for column in range(len(rows)):
            grid = []
            grid.append(rows[row][column])
            #print("First column added")
            try:
                grid.append(rows[row + 1][column])
                #print("Second column added")
            except IndexError:
                grid.append([0] * 3)
            try:
                grid.append(rows[row + 2][column])
                #print("Third column added")
            except IndexError:
                grid.append([0] * 3)
            grids_row.append(grid)
        grids.append(grids_row)

    for value in grids:
        for Grid in value:
            for i in range(0, 3):
                Extend = False
                try:
                    # Checking if list contains a 2nd element
                    Item = Grid[i][1]
                except IndexError:
                    Grid[i].append(0)
                    Extend = True
                try:
                    # Checking if list contains a 3rd element, if item is 0 from the previous statement, another 0 is added
                    Item = Grid[i][2]
                    if Item == 0 and Extend == True:
                        Grid[i].append(0)
                except IndexError:
                    Grid[i].append(0)
            Binary = ""
            try:
                Central = Grid[1][1]
            except:
                Central = 0
            for i in range(len(Grid)):
                for j in range(len(Grid[i])):
                    if j == 1 and i == 1:
                        continue
                    else:
                        if Grid[i][j] < Central:
                            Binary += "0"
                        else:
                            Binary += "1"
            #print(f"Binary for {Grid}: {Binary}")
            LocalBinaryImageList.append(int(Binary, 2))

    for x in range(0, len(LocalBinaryImageList), Height):
        FinalArray.append(LocalBinaryImageList[x:x + Height])

    return FinalArray

def hist(array):

    """
    Inputs:
        array {Type: array[r,c]} Numpy array of the LBP points

    Outputs:
        hist {Type: array} Numpy array of the generated histogram for the points

    """

    array = np.array(array, np.uint8)
    (hist, _) = np.histogram(array.ravel(), bins = np.arange(0,11))
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-6)

    return hist

def euclidian_distance(lbph1,lbph2):

    """
    Inputs:
        lbph1 {Type: array} Numpy array of the generated histogram for the first image  
        lbph2 {Type: array} Numpy array of the generated histogram for the second image

    Outputs:
        distance {Type: Float} Euclidian distance between the points of each histogram
    """

    distance = np.sqrt(np.sum(np.square(lbph1 - lbph2)))
    return distance

def User_IDs(first_name, last_name, storage, LOCAL_IDS, CLOUD_IDS):

    """
    Inputs:
        first_name {Type: String} First name taken from the input text field
        last_name {Type: String} Last name taken from the input text field
        storage {Type: class}
        LOCAL_IDS {Type: Constant}
        CLOUD_IDS {Type: Constant}

    Outputs:
        None
    """


    inputted_name = first_name + " " + last_name
    user_ids = []
    temporary_file = open(LOCAL_IDS, "w")
    temporary_file.close()
    names = []
    exist = False
    try:
        cloud_file = urllib.request.urlopen(
            storage.child(CLOUD_IDS).get_url(None)).read()
    except:
        storage.child(CLOUD_IDS).put(LOCAL_IDS)
        cloud_file = urllib.request.urlopen(
            storage.child(CLOUD_IDS).get_url(None)).read()
    vals = cloud_file.decode("utf-8").split("\r\n")
    for x in vals:
        if x != "":
            element = x.split(" ")
            uuid = element[0]
            name = element[1] + " " + element[2]
            names.append([uuid, name.rstrip()])
            user_ids.append(element[0])
    if len(user_ids) == 0:
        next_user = 1
        user_ids.append(next_user)
    else:
        for x in names:
            if x[1].rstrip() == inputted_name:
                exist = True
        if not exist:
            next_user = int(user_ids[-1]) + 1
            user_ids.append(next_user)
    if not exist:
        name = inputted_name
        File = open(LOCAL_IDS, "a")
        File.write(cloud_file.decode("utf-8"))
        File.write(str(user_ids[-1]) + " " + name + "\n")
        File.close()
        storage.child(CLOUD_IDS).put(LOCAL_IDS)
    os.remove(LOCAL_IDS)
