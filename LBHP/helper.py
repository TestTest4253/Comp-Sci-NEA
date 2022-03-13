import numpy as np
import math


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