import numpy as np
import pandas as pd
import pickle

class Classifior():
  # labels= ['diagonal_2points', 'one_line', 'one_surface']
  def __init__(self,model_path:str):
    self.model_path=model_path
    pass
  
  def set_data(self, raw_data):   # convert it to pd DataFrame
        temp = pd.DataFrame(raw_data)
        self.df = temp
        
  def fft_self(self,df):
    data_rows = df.copy()
    # Apply FFT on each column except the last row
    fft_result = data_rows.apply(lambda col: np.abs(np.fft.fft(col))[:21000], axis=0) # edit this to set the range of the data points
    return fft_result
  
  def processData(self):
    self.df = self.df.iloc[:42000]
    self.df=self.fft_self( self.df)
    return self.df
  
  def load_model(self,mlp_name:str,kpca_name:str):
    mlp_path=self.model_path+mlp_name
    kpca_path=self.model_path+kpca_name
    self.model_clf = pickle.load(open(mlp_path, 'rb'))     
    self.kernel_pca = pickle.load(open(kpca_path, 'rb'))    
    pass
  
  def fit(self):
    input=self.df.copy().T
    input=self.kernel_pca.transform(input)
    return self.model_clf.predict(input)
  
  def predict(self, data):
    df = pd.DataFrame(data)  # convert data to df
    input = df.copy().T
    input = self.kernel_pca.transform(input)
    return self.model_clf.predict(input)

  def predict_label(self):
      # pred = self.predict()
      pred = self.fit()
      labels = ['diagonal_2points', 'one_line', 'one_surface']
      # labels = [0, 1, 2]
      predicted_label = labels[pred[0]]
      print(f"Predicted label: {predicted_label}")
      return predicted_label
  