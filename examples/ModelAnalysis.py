import pickle
import scipy.io as sio
import survivalnet as sn
import data_provider
import numpy as np

# Integrated models.
# Defines model/dataset pairs.
ModelPaths = ['results/']
Models = ['final_model']
Data = ['./survivalData.csv']

# Loads datasets and performs feature analysis.
for i, Path in enumerate(ModelPaths):

    # Loads normalized data.
    Censored, Survival, Normalized, Symbols = data_provider.data_provider(Data[i])

    # Extracts relevant values.
    # Raw = None
    Raw = np.asarray([1, 2, 3]).astype('float32') # Just for parsing something other than None

    # Loads model.
    f = open(Path + Models[i], 'rb')
    Model = pickle.load(f)
    f.close()

    sn.analysis.FeatureAnalysis(Model, Normalized, Raw, Symbols,
                                Survival, Censored,
                                Tau=5e-2, Path=Path)
