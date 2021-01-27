'''

'''

import numpy as np 
from lxml import etree

class VXA:

    def __init__(self, filename=None, body=None):
        self.filename = filename
        self.body = body
        self.write_vxa()

    def write_vxa(self):
        root = etree.XML("<VXA></VXA>")
        self.tree = etree.ElementTree(root)
        root.set('Version', "1.1")

        self.write_sim_xml()
        self.write_env_xml()
        self.write_vxc_xml()

        self.save_xml(self.filename) 

    def write_sim_xml(self):
        pass

    def write_env_xml(self):
        pass

    def write_vxc_xml(self):
        root = self.tree.getroot()
        vxc = etree.SubElement(root, "VXC")
        vxc.set('Version', "0.94")

        palette = etree.SubElement(vxc, "Palette")

        # Muscle 1
        muscle1 = etree.SubElement(palette, "Material")
        muscle1.set('ID', "1")
        self.write_material(muscle1, "Muscle1", rgb=(1,0,0), elastic_mod=100, cte=0.01, material_temp_phase=0)

        # Muscle 2
        muscle2 = etree.SubElement(palette, "Material")
        muscle2.set('ID', "2")
        self.write_material(muscle2, "Muscle2", rgb=(0,1,0), elastic_mod=100, cte=0.01, material_temp_phase=0.5)

        # Bone
        bone = etree.SubElement(palette, "Material")
        bone.set('ID', "3")
        self.write_material(bone, "Bone", rgb=(0,0,1), elastic_mod=500)
        
        # Fat
        fat = etree.SubElement(palette, "Material")
        fat.set('ID', "4")
        self.write_material(fat, "Fat", rgb=(0,1,1), elastic_mod=50)

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
            #TODO: write from 3D array
            pass
        else:
            #TODO: default: single voxel of material 1 
            pass

    def save_xml(self, filename):
        if filename is not None:
            #TODO: set save_fn 
            pass
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
    pass

if __name__=='__main__':
    # If this file is called directly, create a vxa file with a single voxel 
    VXA()

    #TODO: If a vxc file is passed in as a command line argument produce a vxa file with the proper parameters

