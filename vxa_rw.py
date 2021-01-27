'''

'''

import numpy as np 
from lxml import etree

class VXA:

    def __init__(self, body=None):
        self.body = body
        self.write_vxa()

    def write_vxa(self):
        root = etree.XML("<VXA></VXA>")
        self.tree = etree.ElementTree(root)
        root.set('Version', "1.1")

        self.write_sim_xml()
        self.write_env_xml()
        self.write_vxc_xml()

    def write_sim_xml(self):
        root = self.tree.getroot()

        sim = etree.SubElement(root, "Simulator")

        integrator = etree.SubElement(sim, "Integration")
        etree.SubElement(integrator, "DtFrac").text = '0.1'

        damping = etree.SubElement(sim, "Damping")   
        etree.SubElement(damping, "ColDampingZ").text = '0.8'
        etree.SubElement(damping, "SlowDampingZ").text = '0.01' # Ground Damping
        etree.SubElement(damping, "BondDampingZ").text = '1'

        # This doesn't work for some reason
        collisions = etree.SubElement(sim, "Collisions")
        etree.SubElement(collisions, "SelfColEnabled").text = '1'


    def write_env_xml(self):
        root = self.tree.getroot()

        env = etree.SubElement(root, "Environment")

        gravity = etree.SubElement(env, "Gravity")
        etree.SubElement(gravity, "GravEnabled").text = '1'
        etree.SubElement(gravity, "GravAcc").text = '-9.81'
        etree.SubElement(gravity, "FloorEnabled").text = '1'
        
        thermal = etree.SubElement(env, "Thermal")
        etree.SubElement(thermal, "TempEnabled").text = '1'
        etree.SubElement(thermal, "TempAmplitude").text = '15'
        etree.SubElement(thermal, "TempBase").text = '32'
        etree.SubElement(thermal, "VaryTempEnabled").text = '1'
        etree.SubElement(thermal, "TempPeriod").text = '0.3'

    def write_vxc_xml(self):
        root = self.tree.getroot()
        vxc = etree.SubElement(root, "VXC")
        vxc.set('Version', "0.94")

        lattice = etree.SubElement(vxc, "Lattice")
        etree.SubElement(lattice, "Lattice_Dim").text = '0.01'
        etree.SubElement(lattice, "X_Dim_Adj").text = '1'
        etree.SubElement(lattice, "Y_Dim_Adj").text = '1'
        etree.SubElement(lattice, "Z_Dim_Adj").text = '1'
        etree.SubElement(lattice, "X_Line_Offset").text = '0'
        etree.SubElement(lattice, "Y_Line_Offset").text = '0'
        etree.SubElement(lattice, "X_Layer_Offset").text = '0'
        etree.SubElement(lattice, "Y_Layer_Offset").text = '0'

        voxel = etree.SubElement(vxc, "Voxel")
        etree.SubElement(voxel, "Voxel_Name").text = 'BOX'
        etree.SubElement(voxel, "X_Squeeze").text = '1'
        etree.SubElement(voxel, "Y_Squeeze").text = '1'
        etree.SubElement(voxel, "Z_Squeeze").text = '1'

        palette = etree.SubElement(vxc, "Palette")

        # Muscle 1
        muscle1 = etree.SubElement(palette, "Material")
        muscle1.set('ID', "1")
        self.write_material(muscle1, "Muscle1", rgb=(1,0,0), elastic_mod=1e+8, cte=0.01, material_temp_phase=0)

        # Muscle 2
        muscle2 = etree.SubElement(palette, "Material")
        muscle2.set('ID', "2")
        self.write_material(muscle2, "Muscle2", rgb=(0,1,0), elastic_mod=1e+8, cte=0.01, material_temp_phase=0.5)

        # Bone
        bone = etree.SubElement(palette, "Material")
        bone.set('ID', "3")
        self.write_material(bone, "Bone", rgb=(0,0,1), elastic_mod=5e+8)
        
        # Fat
        fat = etree.SubElement(palette, "Material")
        fat.set('ID', "4")
        self.write_material(fat, "Fat", rgb=(0,1,1), elastic_mod=5e+7)

        structure = etree.SubElement(vxc, "Structure")
        structure.set('Compression', "ASCII_READABLE")

        self.set_data(structure)
        
    def write_material(self, material, name, rgb, elastic_mod, cte=0, material_temp_phase=0, \
        density=1e+06, poissons_ratio=0.35, uStatic=1, uDynamic=0.5):
 
        etree.SubElement(material, "Name").text = name
        display = etree.SubElement(material, "Display")
        etree.SubElement(display, "Red").text = str(rgb[0])
        etree.SubElement(display, "Green").text = str(rgb[1])
        etree.SubElement(display, "Blue").text = str(rgb[2])
        mechanical = etree.SubElement(material, "Mechanical")
        etree.SubElement(mechanical, "Elastic_Mod").text = str(elastic_mod)
        etree.SubElement(mechanical, "Density").text = str(density)
        etree.SubElement(mechanical, "Poissons_Ratio").text = str(poissons_ratio)
        etree.SubElement(mechanical, "CTE").text = str(cte)
        etree.SubElement(mechanical, "MaterialTempPhase").text = str(material_temp_phase)
        etree.SubElement(mechanical, "uStatic").text = str(uStatic)
        etree.SubElement(mechanical, "uDynamic").text = str(uDynamic)

    def set_data(self, structure):
        if self.body is not None:
            X_Voxels, Y_Voxels, Z_Voxels = self.body.shape
            body = self.body
        else:
            # Default: creates 10x10x10 world and places single voxel of Material 1 in the middle
            X_Voxels = 10
            Y_Voxels = 10
            Z_Voxels = 10

            body = np.zeros((X_Voxels, Y_Voxels, Z_Voxels), dtype=int)
            body[X_Voxels//2, Y_Voxels//2, 0]=1
            
        etree.SubElement(structure, "X_Voxels").text = str(X_Voxels)
        etree.SubElement(structure, "Y_Voxels").text = str(Y_Voxels)
        etree.SubElement(structure, "Z_Voxels").text = str(Z_Voxels)

        body_flatten = np.zeros((X_Voxels*Y_Voxels, Z_Voxels),dtype=np.int8)
        for i in range(Z_Voxels):
            body_flatten[:,i] = body[:,:,i].flatten()

        Data = etree.SubElement(structure, "Data")
        for i in range(Z_Voxels):
            string = "".join([f"{c}" for c in body_flatten[:,i]])
            etree.SubElement(Data, "Layer").text = etree.CDATA(string)

    def save_xml(self, filename=None):
        if filename is not None:
            save_fn = filename
        else:
            save_fn = 'a.vxa'

        with open('{}'.format(save_fn), 'w+') as f:
            f.write(etree.tostring(self.tree, encoding="unicode", pretty_print=True))

def vxa_from_array(body, save_filename=None):
    '''
    Function to be called from another script 
    Generates and saves a vxa file with the proper parameters and sets the data to the specified 3Darray called body
    Parameters:
        body (numpy.ndarray): 3D numpy array in the form (X_Voxels, Y_Voxels, Z_Voxels)
        save_filename (str): filename for the resulting vxa file (optional)
    '''
    #TODO: exception handling
    # make sure body is a 3D numpy array
    vxa = VXA(body=body)
    vxa.save_xml(save_filename)


if __name__=='__main__':
    # If this file is called directly, create a vxa file with a single voxel 
    vxa = VXA()
    vxa.save_xml()

