import h5py
filename = "IC.hdf5"
with h5py.File(filename, "r") as f:
    print("Keys: %s" % f.keys())
    sate = f['satellites']
    print(list(sate["Coordinates"]))