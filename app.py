from scipy.optimize import linprog
from numpy import reshape
from flask import Flask, render_template, request



app= Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    _N_vars=5
    _N_rest=5
    A_ub=[]
    A_eq=[]
    B_ub=[]
    B_eq=[]
    sol=0
    if request.method == 'POST':
        coef = request.form.getlist('coef[]')
        coef=[float(i) for i in coef]
        type = request.form.getlist('type[]')
        obj = request.form.getlist('obj[]')
        obj=[float(i) for i in obj]
        z = request.form.getlist('func[]')
        z=[float(i) for i in z]
        problem_type=request.form.get('minmax')
        left_bounds=request.form.getlist('l_bounds[]')
        right_bounds=request.form.getlist('r_bounds[]')
        
        bounds=[]
        for i in range(len(left_bounds)):
            if left_bounds[i]=='None' and right_bounds[i]!='None':
                bounds.append([None, right_bounds[i]])
            if left_bounds[i]!='None' and right_bounds[i]=='None':
                bounds.append([left_bounds[i], None])
            if left_bounds[i]!='None' and right_bounds[i]!='None':
                bounds.append([left_bounds[i], right_bounds[i]])
            

        #inverts sign of target function if objective is to maximice
        if problem_type=='maximice':
            z=[float(i)*-1 for i in z]
        coef=reshape(coef, (_N_rest,_N_vars))
        coef=coef.tolist()
        #if you only want to change number of variables or restrictions, leave everything else blank
        if len(coef)>0:
            #this for gets values on inputs, used to get coefficient values 
            for i in range(len(type)):
                if type[i]=='eq':
                    A_eq.append(coef[i])
                    B_eq.append(obj[i])
                if type[i]=='leq':
                    A_ub.append(coef[i])
                    B_ub.append(obj[i])
                if type[i]=='geq':
                    neg=list(coef[i])
                    for j in range(len(neg)):
                        neg[j]=-1*neg[j]
                    A_ub.append(neg)
                    neg=obj[i]*-1
                    B_ub.append(neg)
            if len(A_ub)>0 and len(A_eq)>0:
                sol=linprog(z, A_ub=A_ub, b_ub=B_ub, A_eq=A_eq, b_eq=B_eq,\
                method='revised simplex',bounds=bounds)
                print(sol)
            if len(A_ub)>0 and len(A_eq)==0:
                sol=linprog(z, A_ub=A_ub, b_ub=B_ub,method='revised simplex',bounds=bounds)
                print(sol)
            if len(A_ub)==0:
                sol=linprog(z, A_eq=A_eq, b_eq=B_eq,method='revised simplex',bounds=bounds)
                print(sol)
    return render_template('index.html',N_vars=_N_vars,N_rest=_N_rest,message=sol)
















 
if __name__ == '__main__':    
    app.run(debug=True)