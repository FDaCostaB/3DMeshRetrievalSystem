from ortools.linear_solver import pywraplp
import numpy as np
import pandas as pd
import os
from Settings import settings, settingsName


def read_data_model():
    df = pd.read_csv(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), "catAvg.csv"))
    catFeatMat = np.zeros((df.shape[0],df.shape[1]-2))
    colLabel = []
    newRowLabel = []
    for i, row in df.iterrows():
        newRowLabel.append(row['Pair'])
        j = 0
        for colName in df.columns:
            if colName!='Unnamed: 0' and colName!='Pair':
                catFeatMat[i][j] = round(row[colName]*10,5)
                if i==0: colLabel.append(colName)
                j+=1
    constraintCoeffs = np.zeros((catFeatMat.shape[0], catFeatMat.shape[1]+catFeatMat.shape[0]))

    data = {}
    data['bounds'] = np.zeros(constraintCoeffs.shape[0])
    for i in range(catFeatMat.shape[0]):
        for j in range(catFeatMat.shape[1]):
            constraintCoeffs[i][j] = catFeatMat[i, j]
    for l in range(len(newRowLabel)):
        constraintCoeffs[l, l+catFeatMat.shape[1]] = -1
        colLabel.append(newRowLabel[l])
    data['constraint_coeffs'] = constraintCoeffs

    data['obj_coeffs'] = np.ones(constraintCoeffs.shape[1])
    for i in range(catFeatMat.shape[1]):
        data['obj_coeffs'][i] = 0
    data['obj_coeffs'][len(data['obj_coeffs'])-1]=1
    for i in range(catFeatMat.shape[1],constraintCoeffs.shape[1]):
        if newRowLabel[i-catFeatMat.shape[1]].split('-')[0]==newRowLabel[i-catFeatMat.shape[1]].split('-')[1]:
            data['obj_coeffs'][i]*=-9 # 171/19 unbias the difference between the number of same class comparison (19) and different class comparison (2 chosen in 19)

    data['num_vars'] = constraintCoeffs.shape[1]
    data['num_constraints'] = constraintCoeffs.shape[0]
    return data, newRowLabel, colLabel

def ScalarOptimisedWeight():
    data, rowLabel, colLabel = read_data_model()

    # Instantiate a Glop solver, naming it LinearExample.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    # solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return

    x = {}
    for j in range(data['num_vars']):
        if j<13:
            x[j] = solver.IntVar(0, 11, 'x[%i]' % j)
        else:
            x[j] = solver.IntVar(0, 100, 'x[%i]' % j)
    print('Number of variables =', solver.NumVariables())

    for i in range(data['num_constraints']):
        constraint_expr = [data['constraint_coeffs'][i][j] * x[j] for j in range(data['num_vars'])]
        if data['obj_coeffs'][i+13]<0:
            solver.Add(sum(constraint_expr) <= data['bounds'][i])
        else:
            solver.Add(sum(constraint_expr) >= data['bounds'][i])

    print('Number of constraints =', solver.NumConstraints())

    obj_expr = [data['obj_coeffs'][j] * x[j] for j in range(data['num_vars'])]
    solver.Maximize(solver.Sum(obj_expr))

    # Solve the system.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('\nSolution:')
        print('Objective value =', solver.Objective().Value())
        for j in range(13):
            if j == 13: print('\nCategory distance : ')
            print(colLabel[j], ' = ', x[j].solution_value())
    else:
        print('The problem does not have an optimal solution.')