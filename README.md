# voxcraft-viz-vxa-generator

`vxa_generator.py` is a simple script that generates a `.vxa` file that can be used to load stable parameters into [voxcraft-viz](https://github.com/voxcraft/voxcraft-viz) to visualize voxelbots composed of two materials: active (actuating) voxels and passive voxels. 

## Usage

### Running `vxa_generator.py` directly

The script can be directly run in which case it produces a file named `a.vxa` with a single actuating voxel. This file can then be passed into voxcraft-viz for visualization. For example:

```
python vxa_generator.py
voxcraft-viz a.vxa
```

You can then go into draw mode to draw a robot and visualize it in the Physics Sandbox with the stable parameters set by `a.vxa`.

### Calling `vxa_from_array()` from another script

The script can also be used to load in a robot body specified by a 3-Dimensional NumPy array. In this case, the function `vxa_from_array()` can be called from a different program with the 3D body array as an argument. This produces a `.vxa` file with the specified body and stable parameters. The filename can be specified, otherwise it will be `a.vxa`. For example, suppose we have the following script `my_bot.py`:

```
import numpy as np
from vxa_generator import vxa_from_array

body = np.zeros((2,2,2)) # body is a 2x2x2 cube
body[:,:,0]=1 # bottom layer is active 
body[:,:,1]=2 # top layer is passive

vxa_from_array(body, save_filename='my_bot.vxa')
```

We can run the above script and pass in the resulting `.vxa` file into voxcraft-viz to visualize our bot as follows:

```
python my_bot.py
voxcraft-viz my_bot.vxa
```

## Issues

You have to enable self collisions yourself by clicking the `Enable Self Collision` check box in the Physics Settings. 
