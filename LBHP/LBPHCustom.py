import numpy as np
from PIL import Image
import cv2
from matplotlib import pyplot as plt
import math

Image = np.array(Image.open("645399.jpg"))
print("RUNNING")
GreyImage = cv2.cvtColor(Image, cv2.COLOR_RGB2GRAY)
GreyImageList = GreyImage.tolist()
LocalBinaryImageList = []
Width, Height = math.ceil((len(GreyImageList[0]))), math.ceil((len(GreyImageList))) # Getting the dimensions of the image in terms of grid size 
def get_grids(array):
    SingleRow = []
    rows = []
    Row = []
    grids = []
    # Splits photo into 3 long groupings
    for row in range(len(array)):
        for column in range(len(array)):
            SingleRow.append(array[row][column:column+3])
        SingleRow.append("NEW LINE")
    for x in range(len(SingleRow)):
        if SingleRow[x] == "NEW LINE":
            rows.append(Row)
            Row = []
        else:
            Row.append(SingleRow[x])
    
    # Splits groupings into grids of 1x1 arrays        
    for row in range(len(rows)):
        grids_row = []
        for column in range(len(rows)):
            grid = []
            grid.append(rows[row][column])
            #print("First column added")
            try:
                grid.append(rows[row+1][column])
                #print("Second column added")
            except IndexError:
                grid.append([0]*3)
            try:
                grid.append(rows[row+2][column])
                #print("Third column added")
            except IndexError:
                grid.append([0]*3)
            grids_row.append(grid)
        grids.append(grids_row)
    return grids
Grey_grid = get_grids(GreyImageList)

for value in Grey_grid:
    for Grid in value:
        for i in range(0,3):
            Extend = False
            try:
                Item = Grid[i][1] # Checking if list contains a 2nd element
            except IndexError:
                Grid[i].append(0)
                Extend = True
            try:
                Item = Grid[i][2] # Checking if list contains a 3rd element, if item is 0 from the previous statement, another 0 is added
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
                if j==1 and i==1:
                    continue
                else:
                    if Grid[i][j] < Central:
                        Binary += "0"     
                    else:
                        Binary += "1"
        #print(f"Binary for {Grid}: {Binary}")
        LocalBinaryImageList.append(int(Binary, 2))
#print(LocalBinaryImageList)
NormalisedLocalBinaryImage = []
for x in range(0,len(LocalBinaryImageList), Height):
    NormalisedLocalBinaryImage.append(LocalBinaryImageList[x:x+Height]) # Reformatting list

plt.imshow(np.array(NormalisedLocalBinaryImage, np.uint8),cmap = "gray",vmin = 0, vmax = 255)
plt.show()
