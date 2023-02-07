'''
Seamcarve Homework

The code in this file does the following:
1. It takes in an image (filename in the same directory),
2. Reads it into a 3D array,
3. Processes the 3D array to extract the RGB colors, 
4. Computes the cell costs (color deltas) to produce a 2D array of importance values, and
4. Uses Dynamic Programming to produce the lowest-cost seam as an array of column ids to cut. 
'''
from importance_calculator import ImportanceCalculator
from PIL import Image
import numpy as np
import argparse
import copy

class SeamCarve:
    '''
    This is a class that contains code for finding the "least important" seams,
    and apply it to image resizing.

    Fields:
    image_array: the 3-d (width, height, RGB) array representing the input image
    image_height: the height of the input image, in pixels
    image_width: the width of the input image, in pixels
    dirs: the 2-d dirs array (as described in the handout)
    costs: the 2-d costs array (as described in the handout)

    TODO: There are two methods you need to fill out:
        1. argmin(self, array), and 
        2. find_least_important_seam(self, vals)
    '''
    def __init__(self, image_path: str = None, image_matrix: list = None):
        '''
        Initialization method for the SeamCarve class.

        DO NOT EDIT this method.
        '''
        if (image_path is not None and image_matrix is None):
            # Convert an input image to a 3D array (row (height), column
            # (width), color value (RGBA))
            # image file path has to be in the same directory
            self.image_array = np.array(Image.open(image_path)) 
        elif (image_matrix is not None):
            self.image_array = np.array(image_matrix)
        else:
            raise RuntimeError("Constructor must provide either an image path \
                or image array")

        # get the number of rows (height dimension)
        self.image_height = len(self.image_array) 

        # get the number of columns (width dimension)
        self.image_width = len(self.image_array[0]) 

        if (self.image_height < 2 or self.image_width < 2):
            raise ValueError("Image provided must be at least 2x2 pixels")
        
        self.dirs = None
        self.costs = None

    def argmin(self, array: list[int]) -> int:
        '''
        Returns the minimum element's *index* of a given row (not the element
        itself)

        Parameters: array -- a 1-D array representing a single row of the image.

        Returns: a number -- the minimum element's INDEX in the given row. For
        ties, use the smallest index.

        TODO: Fill in this method
        '''
        return array.index(min(array))
        pass

    def find_least_important_seam(self, vals) -> list[int]:
        '''
        Given a 2D array of importance values, this method finds the "least
        important seam" using the seamcarve algorithm and dynamic programming.

        Parameters: vals -- a 2D array storing "importance values", where an
        importance value indicates how much color contrast a pixel has with its
        neighbors.

        Returns: A least-important seam in the image that is most unlikely to
        cause change in the original image when taken out. The format of this
        seam is an array of pixel positions, where the first element is the
        position of the pixel to be removed in the top row of the image, the
        second is the pixel in the second row, and so on. The leftmost pixel in
        each row corresponds to position 0.

        TODO: Fill in this method
        '''
        # initialize a 2D array with the same dimensions as vals (input) to
        self.costs=[[0]*(len(vals[0])) for _ in range(len(vals))]
        self.dirs=self.dirs=[[0]*(len(vals[0])) for _ in range(len(vals))]
        for i in range(len(vals)-1,-1,-1):
            for k in range(len(vals[0])):
                if i==len(vals)-1:
                    self.costs[i][k]=vals[i][k]
                elif k==len(vals[0])-1:
                    mincost=min(self.costs[i+1][k],self.costs[i+1][k-1])
                    self.costs[i][k]=mincost+vals[i][k]
                    if mincost==self.costs[i+1][k]:
                        self.dirs[i][k]=0
                    else:
                        self.dirs[i][k]=-1
                elif k==0:
                    mincost=min(self.costs[i+1][k],self.costs[i+1][k+1])
                    self.costs[i][k]=mincost+vals[i][k]
                    if mincost==self.costs[i+1][k]:
                        self.dirs[i][k]=0
                    else:
                        self.dirs[i][k]=1
                else:
                    mincost=min(self.costs[i+1][k-1],self.costs[i+1][k],self.costs[i+1][k+1])
                    if mincost==self.costs[i+1][k-1]:
                        self.dirs[i][k]=-1
                    elif mincost==self.costs[i+1][k]:
                        self.dirs[i][k]=0
                    else:
                        self.dirs[i][k]=1
                    self.costs[i][k]=mincost+vals[i][k]
        seam=[self.argmin(self.costs[0])]
        for i in range(len(vals)-1):
            seam.append(seam[i]+self.dirs[i][seam[i]])
        return seam # TODO: return a seam

    def calculate_importance_values(self):
        '''
        Uses the ImportanceCalculator class to calculate the importance values
        for each pixel in the image

        Returns: the 2D array of calculated importance values for each pixel

        DO NOT EDIT this method.
        '''
        importance_calc = ImportanceCalculator(self.image_array)
        return importance_calc.calculate_importance_values()

    def check_bounds(self, for_row: int, for_col: int) -> bool:
        '''
        Helper method to check if the given coordinate is out of bounds. 

        Returns: A boolean -- True if the passed in coordinate is within the
        image's bounds, else return False.

        DO NOT EDIT this method.
        '''
        if for_row < 0 or for_row >= self.image_height or for_col < 0 or\
            for_col >= self.image_width:
            return False # out of bounds
        return True # else, this coordinate is within bounds.


################################################################################
#################### DO NOT MODIFY ANY CODE BELOW THIS LINE ####################
################################################################################

def parse_args():
    '''
    Parses command line arguments for image file path and number of seams carved
    
    '''
    parser = argparse.ArgumentParser(
        description="for running seamcarve on a chosen image!",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--path',
        default='seamcarve_images/example01.png',
        help='''The file path of our chosen image'''
    )
    parser.add_argument(
        '--seamcount',
        default=1,
        help='''The number of seams we want to identify'''
    )

    return parser.parse_args()

# This is the main method that runs the program
if __name__ == "__main__":
    ARGS = parse_args()

    # create instance of seamcarve class with given image
    mySeamCarve = SeamCarve(image_path = ARGS.path)

    # create copy of image array to crop seam by seam
    carved_array = copy.deepcopy(mySeamCarve.image_array)

    # carve the given number of seams out (default 1)
    for i in range(int(ARGS.seamcount)):
        # Actual production of the least important seam below, using all of the
        # helper methods
        # calculate importance values using the input image array
        importance_array = mySeamCarve.calculate_importance_values() 
        # then, find the lowest-cost (least important) seam, in the form of a 1D
        # array of column ids.
        seam = mySeamCarve.find_least_important_seam(importance_array) 
        print("imp array", importance_array)
        print("seam", seam)
        # get current dimensions
        r, c, k = carved_array.shape

        # make a mask of pixels to remove
        mask = np.ones((r, c), dtype=np.bool)

        # deal with seam not found case
        if seam is None:
            print("seam not found!")
        else:
            # Visualize the seam with a white color (255, 255, 255, 255) (RGBA)
            # For a bright image, you can use black (0, 0, 0, 255) instead
            for row in range(mySeamCarve.image_height): # for every row,
                # get column index for that row (column id to cut)
                column_index_to_cut = seam[row] 
                # make it white
                mySeamCarve.image_array[row][column_index_to_cut][0] = 200
                mySeamCarve.image_array[row][column_index_to_cut][1] = 200
                mySeamCarve.image_array[row][column_index_to_cut][2] = 200
                mask[row][column_index_to_cut-i] = False
            # stack the mask to match number of channels in image
            mask = np.stack([mask]*k, axis=2)
            # carve a seam out
            carved_array = carved_array[mask].reshape((r, c -  1, k))

    # show image with seams overlaying it
    img = Image.fromarray(mySeamCarve.image_array)
    img.show()

    # show image with seams carved out
    img = Image.fromarray(carved_array)
    img.show()
