from pulp import *

def IrrigationOpti(Data):
    Lp_Problem = LpProblem("Irrigaton Optimization",LpMinimize)
    crops = []
    for i in range(len(Data['Crops'])):
        temp_variable = LpVariable(i)
        crops.append(i)
    Lp_Problem += [i in crops]
    for i in range(len(crops)):
        Lp_Problem += crops[i] >= data['ResW'] -data['RainW'] - data['SM'] + data['DW']
        Lp_Problem += crops[i] <= data['ResWM'] -data['RainW'] - data['SM'] + data['DW']
        Lp_Problem += data['RainWM'] + data['SW'] + crops[i] - data['DW'] >= data['NW']
    pass

def IrrigationOptimize(data):
    Lp_Problem = LpProblem("Irrigaton Optimization",LpMinimize)
    x1 = LpVariable(data['crops'][0])
    x2 = LpVariable(data['crops'][1])
    Lp_Problem += data['Area'][0] * x1 + data['Area'][1] * x2 <= data['IW']
    Lp_Problem += x1 + x2 , "Z"
    Lp_Problem += x1 >= data['ResW'] -data['RainW'] - data['SM'] + data['DW']
    Lp_Problem += x1 <= data['ResWM'] -data['RainW'] - data['SM'] + data['DW']
    Lp_Problem += data['RainWM'] + data['SM'] + x1 - data['DW'] >= data['NW'][0]
    Lp_Problem += x2 >= data['ResW'] -data['RainW'] - data['SM'] + data['DW']
    Lp_Problem += x2 <= data['ResWM'] -data['RainW'] - data['SM'] + data['DW']
    Lp_Problem += data['RainWM'] + data['SM'] + x2 - data['DW'] >= data['NW'][1]
   # print(Lp_Problem)
   # print(LpStatus[Lp_Problem.status])
    Lp_Problem.solve()
    ProblemStatus = LpStatus[Lp_Problem.status]
    ObjectiveValue = pulp.value(Lp_Problem.objective)
    variable = {}
    for var in Lp_Problem.variables():
        variable[var.name] = var.varValue

    return ({'Status':ProblemStatus,'ObjectiveValue':ObjectiveValue,'Values':variable })

data = {
    'crops':['Alu','Peda'],
    'Area':[400,700],
    'ResW':200,
    'RainW':15,
    'RainWM':15,
    'SM':12,
    'DW':25,
    'NW':[100,30],
    'ResWM':400,
    'IW':1200000
}

#IrrigationOptimize(data)