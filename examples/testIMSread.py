# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 13:06:06 2019

@author: esol
"""
import pyims

#https://git.equinor.com/ProcessControl/pyIMS
 
print(pyims.list_aspen_servers())
#print(pyims.list_pi_servers())
c = pyims.IMSClient('GFA','Aspen')
#c = pyims.IMSClient('GRA','Aspen')
c.connect() 
tags = ['GFA.27-TT___215_.PV','GFA.27-PT___180_.PV','GFA.40-TT___069_.PV','GFA.40-PT___074_.PV','GFA.27-TIC__215_.OUT','GFA.27-XV___167_.CMD','GFA.27-XV___167_.ZSH','GFA.27-ZT___167_.PV','GFA.27-FI___165B.PV','GFA.27-TT___130_.PV','GFA.27-TT___181_.PV','GFA.27-FIC__165_.PV'] 

df = c.read_tags(tags,'20-May-19 13:00:00','06-Jun-19 13:00:00',3600) 
df.describe()

print(df.head(5))

print(c.search_tag('*GFA*TT*'))



from neqsim.thermo import fluid, TPflash

# Start by creating a fluid in neqsim
fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
fluid1.setTemperature(28.15, "C")
fluid1.setPressure(10.0, "bara")
fluid1.addComponent("methane", 10.0, "mol/sec")
fluid1.setMixingRule(2)
TPflash(fluid1)

def density(temperature):
        fluid1.setTemperature(temperature+273.15)
        fluid1.init(1)
        fluid1.initPhysicalProperties()
        return fluid1.getDensity("kg/m3")

dataTest = df[["GFA.27-PT___180_.PV", "GFA.40-TT___069_.PV"]]
dataTest["GFA.27-PT___180_.PV"].apply(density)




"""
# Load libraries
import pandas
from sklearn import model_selection
# Split-out validation dataset
array = dataTest.values
X = array[:,0:3]
Y = array[:,3]
validation_size = 0.20
seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
#clf = LogisticRegression()
#clf.fit(X_train, Y_train)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.svm import SVR

#clf = LinearRegression()
clf = SVR(kernel='linear')
clf.fit(X_train, Y_train)

print("preditions::")
print(clf.predict(X_validation))
predictions = clf.predict(X_validation)
res = clf.predict(X_validation)
print("Accuracy " + str(clf.score(X_validation, Y_validation)))
r2_score(res,Y_validation )
"""