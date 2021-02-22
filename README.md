# voxcraft-viz-vxa-generator

`vxa_generator.py` is a simple script that generates a `.vxa` file that can be used to load stable parameters into [voxcraft-viz](https://github.com/voxcraft/voxcraft-viz) to visualize voxelbots composed of two materials: active (actuating) voxels and passive voxels. 

For more information on voxcraft-viz and for installation instructions see here: https://voxcraft.github.io/design#viz

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

## Designing bots

#### 1. Drawing in voxcraft-viz
To use draw mode in voxcraft-viz to design a bot you can first use `vxa_generator.py` to load in stable parameters for visualization after drawing. In this case, first run `vxa_generator.py` which produces a file called `a.vxa`. Pass this file into voxcraft-viz to load in the parameters as follows:

```
python vxa_generator.py
voxcraft-viz a.vxa
```

This will open voxcraft-viz with a default bot of a single actuating voxel. You can then go into draw mode to design a morphology and test your design in the physics sandbox without needing to tune parameters.

If you find a design you like be sure to export the `.vxc` file from voxcraft-viz to save your design. To re-load your saved design, you can pass it back into `vxa_generator.py` to generate a `.vxa` file for your design with the stable parameters.

```
python vxa_generator.py my_saved_bot.vxc
voxcraft-viz my_saved_bot.vxa
```

Note: You can always load a bot with stable parameters into voxcraft-viz from any saved `.vxc` file. To do so, you must first generate the corresponding `.vxa` file using `viz_generator.py`. 
```
python vxa_generator.py any_bot.vxc
voxcraft-viz any_bot.vxa
```

[Draw bot demo video](https://youtu.be/UDvGwAs_9pc)

#### 2. Random bot generator
Alternatively, you can generate random designs using `random_bot.py`. Running this script will produce a file called `random_bot.vxa` that can be visualized in voxcraft-viz as follows:

```
python random_bot.py
voxcraft-viz random_bot.vxa
```
You can alter the dimensions of the bot by changing the `WORKSPACE_LENGTH` variable in `random_boy.py`.

[Random bot demo video](https://youtu.be/XkhRblonPs8)

## Notes

To enable self collisions you have to do so yourself by clicking the `Enable Self Collision` check box in the Physics Settings. 
