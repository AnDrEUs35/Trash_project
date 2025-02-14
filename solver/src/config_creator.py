#imports
import numpy as np
import h5py
import json
import os


class Config_cretor:
    
    def __init__(self, data, output_path):

        self.output_path = output_path

        self.FloatType = np.float64
        self.IntType = np.int32
        self.BoxSize = self.FloatType(150000) # км, размер области моделирования

        with open(data, 'r') as file:
            self.data = json.load(file)

        # Конфигурационные файлы для моделирования, необходимые 
        # библиотеке AREPO code. Вся информация в этих файлах статична,
        # поскольку моделирование зависит только от расположения 
        # частиц (спуников, мусора и т.п.)
        os.system(f'cp ./param.txt {self.output_path}/param.txt')
        os.system(f'cp ./Config.sh {self.output_path}/Config.sh')
    
    def get_hdf5(self):
        # return './../test/IC.hdf5'

        # open file
        IC = h5py.File(f'{self.output_path}/IC.hdf5', 'w')
        header = IC.create_group("Header")

        # Earth parametrs
        mass_earth = np.array([5.6e24])
        pos_earth = np.zeros([1, 3], dtype=self.FloatType) + self.BoxSize / 2
        vel_earth = np.zeros([1, 3], dtype=self.FloatType)
        part3 = IC.create_group("PartType3") # Earth
        
        if 'filtered_objects' in self.data:
            part1 = IC.create_group("PartType1") # filtered_objects

            # filtered_objects parametrs
            n_sat = len(self.data['filtered_objects'])
            sat_names = np.array([self.data['filtered_objects'][i]['name'] for i in range(n_sat)])
            pos_sattelite = np.zeros([n_sat, 3], dtype=self.FloatType) + self.BoxSize / 2
            vel_sattelite = np.zeros([n_sat, 3], dtype=self.FloatType)
            mass_sat = np.ones(n_sat, dtype=self.FloatType)
            
            # filling pos and vel of filtered_objects and trash
            for i in range(n_sat):
                for j in range(3):
                    pos_sattelite[i][j] += self.FloatType(self.data['filtered_objects'][i]['coords'][j])
                    vel_sattelite[i][j] = self.FloatType(self.data['filtered_objects'][i]['velocity'][j])
        else:
            n_sat = 0

        if 'trash' in self.data:
            part2 = IC.create_group("PartType2") # trash

            # trash parametrs
            n_tr = len(self.data['trash'])
            tr_indexes = np.array([self.data['trash'][i]['name'] for i in range(n_tr)])
            pos_trash = np.zeros([n_tr, 3], dtype=self.FloatType)
            vel_trash = np.zeros([n_tr, 3], dtype=self.FloatType)
            mass_trash = np.ones(n_tr, dtype=self.FloatType)

            for i in range(n_tr):
                for j in range(3):
                    pos_trash[i][j] = self.FloatType(self.data['trash'][i]['coords'][j])
                    vel_trash[i][j] = self.FloatType(self.data['trash'][i]['velocity'][j])
        else:
            n_tr = 0

        # part4 = IC.create_group("PartType4") # User_satellite
        
        #header
        NumPart = np.array([0, n_sat, n_tr, 1, 0, 0], dtype = self.IntType)
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
        
        try:
            #filtered_objects
            part1.create_dataset("ParticleIDs", data=np.arange(1, n_sat + 1))
            part1.create_dataset("Coordinates", data=pos_sattelite)
            part1.create_dataset("Masses", data=mass_sat)
            part1.create_dataset("Velocities", data=vel_sattelite)
        except:
            pass
        
        try:
            # trash
            part2.create_dataset("ParticleIDs", data=np.arange(n_sat + 1, n_sat + n_tr + 1))
            part2.create_dataset("Coordinates", data=pos_trash)
            part2.create_dataset("Masses", data=mass_trash)
            part2.create_dataset("Velocities", data=vel_trash)
        except:
            pass
        
        # Earth
        part3.create_dataset("ParticleIDs", data=np.arange(0, 1))
        part3.create_dataset("Coordinates", data=pos_earth)
        part3.create_dataset("Masses", data=mass_earth)
        part3.create_dataset("Velocities", data=vel_earth)
        
        # close file
        IC.close()
