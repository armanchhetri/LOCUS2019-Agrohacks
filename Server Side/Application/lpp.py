from pulp import *

from model import User, Dairy, Crops
def solve_dairy(user_id, bound):
    prob = LpProblem("Dairy", LpMaximize)
    x1 = LpVariable("x1",lowBound=0)
    x2 = LpVariable("x2",lowBound=0)
    x3 = LpVariable("x3",lowBound=0)
    x4 = LpVariable("x4",lowBound=0)
    cons=Dairy.query.filter_by(user=user_id)

    prob+=cons[3].milk*x1 + cons[3].ghee*x2 + cons[3].curd*x3 + cons[3].cheese*x4
    prob+=cons[0].milk*x1 + cons[0].ghee*x2 + cons[0].curd*x3 + cons[0].cheese*x4 <=bound[0]
    prob+=cons[1].milk*x1 + cons[1].ghee*x2 + cons[1].curd*x3 + cons[1].cheese*x4 <=bound[1]
    prob+=cons[2].milk*x1 + cons[2].ghee*x2 + cons[2].curd*x3 + cons[2].cheese*x4 <=bound[2]
    prob+=1*x1 + 0*x2 + 0*x3 +0*x4 <=150
    prob+=0*x1 + 1*x2 + 0*x3 +0*x4 <=100
    prob+=0*x1 + 0*x2 + 1*x3 +0*x4 <=140
    prob+=0*x1 + 0*x2 + 0*x3 +1*x4 <=75

    status=prob.solve()
    if LpStatus[status]=='Optimal':
        result=[value(x1),value(x2),value(x3),value(x4),value(prob.objective)]
        return result

    else:
        return "No optimal solution"



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

def Neededwater(crop,stages):
    try:
        valueCrop = Crops.query.filter_by(Name = crop).first()
        water = valueCrop.water_requirement
    except:
        return 10
    Neededwater =  water/1000
    rootdepth_seedling = valueCrop.rootdepth_seedling
    rootdepth_vegetative = valueCrop.rootdepth_vegetative
    rootdepth_flowing = valueCrop.rootdepth_flowing
    if stages == 1:
        return (Neededwater/rootdepth_flowing)
    elif stages == 2:
        return  (Neededwater/rootdepth_seedling)
    else:
        return (Neededwater/rootdepth_vegetative)
        

   