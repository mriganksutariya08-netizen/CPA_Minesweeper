how to run:

go to minesweeperonline.com

using get_mouse_position get the pixel value of the top left corner

add respective values to BOARD_COORDS, define DIFFICULTY

then run mouse_control


other tips:

dont zoom in the browser!!!!!!!
anti aliasing issues

on my laptop at 1920 x 1080
at 200% zoom the tiles are 32 px



code info:

grid_data makes nested list for box values

get_neighbours() gives list of 8 surround boxes -
yet to make a case for error for edge boxes


now we gotta start with the human type algorithm

29/9
human type algorithm is done