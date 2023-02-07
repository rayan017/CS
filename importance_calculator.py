'''
DO NOT MODIFY THIS CLASS

This is a helper class to calculate the importance values of the pixels in your
image. This class is used in the calculate_importance_values method in
seamcarve.py
'''

class ImportanceCalculator:
    '''
    ImportanceCalculator class. Defines an object (ImportanceCalculator) that
    calculates the importance value for each pixel in the input image
    '''
    def __init__(self, img_array):
        self.image_array = img_array
        self.image_height = len(self.image_array)
        self.image_width = len(self.image_array[0])
        
    def get_single_pixel_color(self, row: int, col: int) -> list[int]:
        '''
        Helper method to extract RGB colors from the image and given row and
        column, disregarding the alpha value

        Parameters: row -- the row of the specified pixel col -- the column of
        the specified pixel

        Returns: array representing the RGB color values of the pixel
        '''
        # array of size 3. order: R, G, B (because we used the PIL module,
        # instead of OpenCV)
        output = [0 for i in range(3)] 
        pixel_r = self.image_array[row][col][0] 
        pixel_g = self.image_array[row][col][1] 
        pixel_b = self.image_array[row][col][2] 
        # we do not need the alpha channel, which is the last element (index 3).
        output[0] = int(pixel_r)
        output[1] = int(pixel_g)
        output[2] = int(pixel_b) # store our pixel colors into the output array

        return output # output is array of RGB color values (length = 3)

    def calculate_importance_values(self):
        '''
        Given an image array, this method calculates the importance value of
        each pixel and stores it in a 2D array

        Returns: a 2D array of calculated importance values stored in each
        element ("pixel")
        '''
        imp_vals = []
        for row in range(0, self.image_height):
            imp_row = []
            for col in range(0, self.image_width):
                imp_row.append(self.get_importance_value(row, col))
            imp_vals.append(imp_row)
        return imp_vals

    def get_importance_value(self, row: int, col: int) -> int:
        '''
        A method to calculate the importance value of an index for "one pixel"
        (not the whole image)

        Parameters: row -- the row of the specified pixel col -- the column of
        the specified pixel

        Returns: a number representing the importance value of that one single
        pixel at (row, col) of the image
        '''

        potential_neighbors = [(row - 1, col), (row + 1, col), (row, col - 1),\
            (row, col + 1)]
        neighbors = [n for n in potential_neighbors if n[0] >= 0 and\
            n[0] < self.image_height and\
                n[1] >= 0 and\
                    n[1] < self.image_width]

        # variable that will store RGBcolors (1D array of size 3)
        curr_pixel_color = self.get_single_pixel_color(row, col)
        importance_val = 0 # initialize importance value as zero (int)
        for (r, c) in neighbors:
            neighbor_pixel_color = self.get_single_pixel_color(r, c)
            for rgb in range(0, 3):
                importance_val += abs(neighbor_pixel_color[rgb] -\
                    curr_pixel_color[rgb])

        return importance_val / len(neighbors)
