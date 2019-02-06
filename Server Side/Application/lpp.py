from pulp import *
from model import User, Dairy
def solve_dairy(user_id, bound):
    prob = LpProblem("Dairy", LpMaximize)
    x1 = LpVariable("x1",lowBound=0)
    x2 = LpVariable("x2",lowBound=0)
    x3 = LpVariable("x3",lowBound=0)
    x4 = LpVariable("x4",lowBound=0)
    cons=Dairy.query.filter_by(user=user_id)

    prob+=cons[3].milk*x1 + cons[3].ghee*x2 + cons[3].curd*x3 + (cons[3].cheese/946.79)*x4
    prob+=cons[0].milk*x1 + cons[0].ghee*x2 + cons[0].curd*x3 + (cons[0].cheese/946.79)*x4 <=bound[0]
    prob+=cons[1].milk*x1 + cons[1].ghee*x2 + cons[1].curd*x3 + (cons[1].cheese/946.79)*x4 <=bound[1]
    prob+=cons[2].milk*x1 + cons[2].ghee*x2 + cons[2].curd*x3 + (cons[2].cheese/946.79)*x4 <=bound[2]
    prob+=1*x1 + 0*x2 + 0*x3 +0*x4 <=300
    prob+=0*x1 + 1*x2 + 0*x3 +0*x4 <=200
    prob+=0*x1 + 0*x2 + 1*x3 +0*x4 <=300
    prob+=0*x1 + 0*x2 + 0*x3 +(1/946.79)*x4 <=15/946.79

    status=prob.solve()
    if LpStatus[status]=='Optimal':
        result=[value(x1),value(x2),value(x3),value(x4),value(prob.objective)]
        return result

    else:
        return "No optimal solution"
