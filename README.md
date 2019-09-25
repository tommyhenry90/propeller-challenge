# Propeller Challenge Attempt - Tommy Henry

## Installation
To install dependencies:
<code>
pip install -r requirements.txt
</code>

To run:
<code>
python3 path/to/file.jpg
</code>

(Tested using python 3.7 on MacOS)

## My Solution
* Runs using the opencv python package
* Works by first converting image to a patrix and 
then using simple matrix operations to split image into 256x256 pixel
tiles. 
* For each tile I then use the built in downsapling tool in open cv to
save half size copies until we have only 1x1 pixel images left and 
save them in the relevant format on the way

### Limitations and Tradeoffs
* Went for simplicity over performance
  * Runs as a linear program so might be a bit slow for larger files
  * Could potentially improve performance with threading?
* Currently only using the default sampling method for downsizing images
There are centainly other sampling methods that could be looked into 
to optimise for different applications
* Realised after testing that when higher level tiled images are reconstructed
they look very pixelated - should change method to fix this -> downsize first
then tile
* With more time I would write more tests to ensure running effectively
 - test against different filetypes
 - test with really large file sizes
 
