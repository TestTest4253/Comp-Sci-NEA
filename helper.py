# For the Texture analysis
import numpy as np
import math
from PIL import Image
import cv2
import matplotlib as plt

# For the Datastore
import os
import pyrebase
import urllib


def local_binary_pattern(image):

    """
    Inputs:
        image {type: Array[r,c]} image of the intended image to be calculated

    Outputs:
        FinalArray {type: List[r,c]} Array of the LBP points for each pixel 
    """
    try:
        image = cv2.cvtColor(np.array(Image.open(image), np.uint8), cv2.COLOR_RGB2GRAY)
    except: 
        image = np.array(Image.open(image), np.uint8)
    Height = math.ceil((len(image)))
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

    # Creates 2D array of the 3 rows
    for row in range(len(rows)):
        grids_row = []
        for column in range(len(rows)):
            grid = []
            grid.append(rows[row][column])
            try:
                grid.append(rows[row + 1][column])
            except IndexError:
                grid.append([0] * 3)
            try:
                grid.append(rows[row + 2][column])
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
                        try:
                            if Grid[i][j] < Central:
                                Binary += "0"
                            else:
                                Binary += "1"
                        except:
                            print("[INFO] Error between lists and strings, rare occurence.")
            LocalBinaryImageList.append(int(Binary, 2))

    for x in range(0, len(LocalBinaryImageList), Height):
        FinalArray.append(LocalBinaryImageList[x:x + Height]) # Splitting long array into arrays of the length of the image

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

def euclidean_distance(lbph1,lbph2):

    """
    Inputs:
        lbph1 {Type: array} Numpy array of the generated histogram for the first image  
        lbph2 {Type: array} Numpy array of the generated histogram for the second image

    Outputs:
        distance {Type: Float} Euclidean distance between the points of each histogram
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
    vals = cloud_file.decode("utf-8").split("\r\n") # Converts the web version to a string format
    for x in vals:
        if x != "":
            element = x.split(" ") # Breaks line into ID and their name
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

def backup_files(storage, directory):
    """
    Inputs:
        storage {Type: class} 
        directory {Type: string} File path for the face directory
    Outputs:
        None
    """
    folders = os.listdir(directory)
    for folder in folders:
        try:
            storage.child(f"Faces/{folder}/myimage1.png").download(
                f"Faces/{folder}/myimage1.png", "Downloaded.txt")
            os.remove("Downloaded.txt")
        except:
            for image in os.listdir(directory+"\\"+folder):
                cloud_path = f"Faces/{folder}/{image}"
                local_path = directory+"\\"+folder+"\\"+image
                storage.child(cloud_path).put(local_path)
                time.sleep(0.15)

def show_hist(hist):
    """
    Inputs:
        np array of the histogram
    Outputs:
        Displays histogram visualisation of given array
    """
    vals = range(len(hist))
    plt.bar(vals, hist)
    plt.axis = ("off")
    plt.title("Person in Image")
    plt.show()