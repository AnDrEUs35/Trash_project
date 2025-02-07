#imports
import numpy as np
import h5py
import json


class Graphica3D:
    
    def __init__(self, data):
        self.BoxSize = 500
        self.FloatType = np.float64
        self.IntType = np.int32
        with open(data, 'r') as file:
            self.data = json.load(file)
    
    def get_hdf5(self, output_path):
        #return './../test/IC.hdf5'
        
        #Earth parametrs
        mass_earth = np.array([5.6e24])
        pos_earth = np.zeros([1, 3], dtype=self.FloatType)
        vel_earth = np.zeros([1, 3], dtype=self.FloatType)
        
        #satellites parametrs
        n_sat = len(self.data['satellites'])
        sat_names = np.array([self.data['satellites'][i]['name'] for i in range(n_sat)])
        pos_sattelite = np.zeros([n_sat, 3], dtype=self.FloatType)
        vel_sattelite = np.zeros([n_sat, 3], dtype=self.FloatType)
        mass_sat = np.ones(n_sat, dtype=self.FloatType)
        
        
        #trash parametrs
        n_tr = len(self.data['trash'])
        tr_indexes = np.array([self.data['trash'][i]['index'] for i in range(n_tr)])
        pos_trash = np.zeros([n_tr, 3], dtype=self.FloatType)
        vel_trash = np.zeros([n_tr, 3], dtype=self.FloatType)
        mass_trash = np.ones(n_tr, dtype=self.FloatType)
        
        
        #filling pos and vel of satellites and trash
        for i in range(n_sat):
            for j in range(3):
                pos_sattelite[i][j] = self.FloatType(self.data['satellites'][i]['coords'][j])
                vel_sattelite[i][j] = self.FloatType(self.data['satellites'][i]['velocity'][j])
        
        for i in range(n_tr):
            for j in range(3):
                pos_trash[i][j] = self.FloatType(self.data['trash'][i]['coords'][j])
                vel_trash[i][j] = self.FloatType(self.data['trash'][i]['velocity'][j])
        
        
        #open file
        IC = h5py.File('/workspaces/Trash_project/solver/test/IC.hdf5', 'w')
        
        #creating groups
        header = IC.create_group("Header")
        part1 = IC.create_group("satellites") #
        part2 = IC.create_group("trash") #
        part3 = IC.create_group("Earth") #
        
        #header
        NumPart = np.array([0, 1, n_tr, 0, 0, 0], dtype = self.IntType)
        header.attrs.create("NumPart_ThisFile", NumPart)
        header.attrs.create("NumPart_Total", NumPart)
        header.attrs.create("NumPart_Total_HighWord", np.zeros(6, dtype = self.IntType))
        header.attrs.create("MassTable", np.zeros(6, dtype = self.IntType))
        header.attrs.create("Time", 0.0)
        header.attrs.create("Redshift", 0.0)
        header.attrs.create("BoxSize", self.BoxSize)
        header.attrs.create("NumFilesPerSnapshot", 1)
        header.attrs.create("Omega0", 0.0)
        header.attrs.create("OmegaB", 0.0)
        header.attrs.create("OmegaLambda", 0.0)
        header.attrs.create("HubbleParam", 1.0)
        header.attrs.create("Flag_Sfr", 0)
        header.attrs.create("Flag_Cooling", 0)
        header.attrs.create("Flag_StellarAge", 0)
        header.attrs.create("Flag_Metals", 0)
        header.attrs.create("Flag_Feedback", 0)
        header.attrs.create("Flag_DoublePrecision", 1)
        
        #satellites
        part1.create_dataset("ParticleIDs", data=np.arange(1, n_sat + 1))
        part1.create_dataset("Coordinates", data=pos_sattelite)
        part1.create_dataset("Masses", data=mass_sat)
        part1.create_dataset("Velocities", data=vel_sattelite)
        
        #trash
        part2.create_dataset("ParticleIDs", data=np.arange(n_sat + 1, n_sat + n_tr + 1))
        part2.create_dataset("Coordinates", data=pos_trash)
        part2.create_dataset("Masses", data=mass_trash)
        part2.create_dataset("Velocities", data=vel_trash)
        
        #Earth
        part3.create_dataset("ParticleIDs", data=np.arange(0, 1))
        part3.create_dataset("Coordinates", data=pos_earth)
        part3.create_dataset("Masses", data=mass_earth)
        part3.create_dataset("Velocities", data=vel_earth)
        
        # close file
        IC.close()
        
    def get_user_graphical_data(self):
        pass
