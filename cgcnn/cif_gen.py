import numpy as np
import pandas as pd
from pymatgen import core
from pymatgen.io import cif

def lattmat(df,ajdi,relaxation_step_number):
    """Create a numpy matrix of lattice vectors. A column = a vector.
    
    Keyword arguments:
    df -- dataframe of the lattice vectors
    ajdi -- id of the material
    relaxation_step_number -- self explanatory
    """
    return np.transpose(df.loc[(df["id"]==ajdi) & (df["relaxation_step_number"]==relaxation_step_number)].loc[:,["lattice_vector_1_x" ,"lattice_vector_1_y" ,"lattice_vector_1_z" ,"lattice_vector_2_x" ,"lattice_vector_2_y" ,"lattice_vector_2_z" ,"lattice_vector_3_x" ,"lattice_vector_3_y", "lattice_vector_3_z"]].to_numpy().reshape(3,3))


def init_material(df_frac, df_latt, ajdi, rsn):
    """Initiate the IStructure class of pymatgen using the data.
    Returns an instance of IStructure for the given material data.

    Keyword arguments:
    df_frac -- dataframe of fractional coordinates of atoms
    df_latt -- dataframe of lattice vectors
    ajdi -- id of the material
    rsn -- relaxation step number of the material
    """
    lattice = np.transpose(lattmat(df_latt,ajdi,rsn)) # pymatgen compatible lattice vector
    species = df_frac[(df_frac["id"]==ajdi) & (df_frac["relaxation_step_number"]==rsn)].species.values
    coords = df_frac[(df_frac["id"]==ajdi) & (df_frac["relaxation_step_number"]==rsn)][df_frac.columns[-3:]].values

    material = core.IStructure(lattice=lattice, species=species, coords=coords, to_unit_cell=True, coords_are_cartesian=False)
    return material



# df_egy_train_path_FINAL =
df_egy_train = pd.read_csv("train/final/energy.csv")
# df_egy_test_path_FINAL =
df_egy_test = pd.read_csv("test/final/energy.csv")

# df_latt_train_path_VEGARD = 
df_latt_train = pd.read_csv("train/start/lattice_vegard.csv")
# df_latt_test_path_VEGARD =
df_latt_test = pd.read_csv("test/start/lattice_vegard.csv")

# df_frac_train_path_VEGARD =
df_frac_train = pd.read_csv("train/start/frac_vegard.csv")
# df_frac_test_path_VEGARD = 
df_frac_test = pd.read_csv("test/start/frac_vegard.csv")

# df_gen_train_path_VEGARD =
df_gen_train = pd.read_csv("train/relaxation/general.csv")
# df_gen_test_path_VEGARD =
df_gen_test = pd.read_csv("test/relaxation/general.csv")

# test on test data first
ajdis = df_gen_test["id"]
indexing = df_latt_test[["id", "relaxation_step_number"]]

for ajdi in ajdis:
    for rsn in indexing[indexing["id"]==ajdi].relaxation_step_number.values:
        material = init_material(df_frac_test, df_latt_test, ajdi, rsn)
        cif_writer = cif.CifWriter(material)
        cif_writer.write_file("cifs_test/" + str(ajdi) + ".cif")
        # Warning: The symmetry group data is wrong - all structures are label P 1

# now train
ajdis = df_gen_train["id"]
indexing = df_latt_train[["id", "relaxation_step_number"]]

for ajdi in ajdis:
    for rsn in indexing[indexing["id"]==ajdi].relaxation_step_number.values:
        material = init_material(df_frac_train, df_latt_train, ajdi, rsn)
        cif_writer = cif.CifWriter(material)
        cif_writer.write_file("cifs_train/" + str(ajdi) + ".cif")
        # Warning: The symmetry group data is wrong - all structures are label P 1
