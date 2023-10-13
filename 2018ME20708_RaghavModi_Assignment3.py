import ast

## THE FOLLOWING SECTION IS MEANT FOR GIVING THE INPUT
## A SAMPLE TEST CASE HAS ALREADY BEEN PUT
## OBJECTIVE FUNCTION CO-EFFICIENTS SHOULD ALSO CONTAIN '0' CORRESSPONDING TO SLACK VARIABLES
## CONSTRAINT MATRIX WILL ALSO CONTAIN SLACK VARIABLES WHICH WILL ALSO FORM THE INITIAL BASIS

objective = [-1,-2,0,0,0]                              ## OBJECTIVE FUNCTION ALONG WITH '0' CORRESSPONDING TO SLACK VARIABLES
constraints = [[-2,1,1,0,0],[-1,2,0,1,0],[1,0,0,0,1]]   ## CONSTRAINT MATRIX ALONG WITH SLACK VARIABLES WHICH WILL ALSO FORM THE INITIAL BASIS
rhs = [2, 7, 3]                                           ## RHS OF EACH CONSTRAINT IN THE FORM OF A VECTOR
m = len(constraints)                                    ## REPRESENTS TOTAL NUMBER OF CONSTRAINTS
n = len(constraints[0])                                 ## REPRESENTS TOTAL NUMBER OF VARIABLES INCLUDING SLACK VARIABLES

## BASIS VECTOR HAS BEEN DEFINED TO REPRESENT THE VARIABLES WHICH FORM THE BASIS
## THE PLACE OF OCCURENCE WILL REPRESENT THE VARIABLE, WOULD BE SAME AS THAT IN CONSTRAINT MATRIX
## THE NUMBER GIVEN THERE WOULD REPRESENT THE ROW OF TABLEAU WHICH WOULD REPRESENT THAT VARIABLE

basis=[]                                                ## BASIS VECTOR
for i in range (n):
    if i < n - m :
        basis.append(0)
    else:
        basis.append(i - n + m + 1)

## THE NEXT TWO FOR LOOPS ARE FOR CONSTRUCTING INITIAL TABLEAU
        
for i in range(m):                                      ## INCLUDE THE RHS IN THE CONSTRAINTS MATRIX AS FIRST STEP IN TABLEAU MAKING                                  
    constraints[i].append(rhs[i])
objective.append(0)                                     ## INITIAL RHS FOR OBJECTIVE FUNCTION WILL BE ZERO

tableau = [objective]                                   ## SET THE OBJECTIVE FUNCTION AS FIRST ROW 
for i in range(m):                                      ## CONSTRAINTS BECOME THE FOLLOWING ROWS IN TABLEAU
    tableau.append(constraints[i])

## FROM HERE ON THE VARIOUS FUNCTIONS WHICH HAVE BEEN USED ARE DEFINED
## AT THE START OF EACH FUNCTION A NUMBER HAS BEEN GIVEN TO EACH FUNCTION

def row_trans(mat, r1, r2, ratio):                      ## function 1
    coloumn = len(mat[0])
    for i in range(coloumn):
        mat[r1][i] = mat[r1][i] + ratio * mat[r2][i]
    return mat 

def enter(mat ,n):                                      ## function 2
    mini = 0
    col = -1
    for i in range(n):
        if mat[0][i] < mini:
            mini = mat[0][i]
            col = i
    return (col)

def leave(mat, col, m, n, basis):                       ## function 3
    ratio = 0
    row = -1
    for i in range (1, m+1):
        a = mat[i][col]
        if a>0:
            b = mat[i][n]/a
        if a>0 and ratio == 0:
            ratio = mat[i][n]/mat[i][col]
            row = i
        if (a>0 and b < ratio):
            ratio = mat[i][n]/mat[i][col]
            row = i
    if mat[row][col]!=1:
        a = 1/mat[row][col]
        mat = row_trans(mat, row, row, a-1)
    for i in range(n):
        if basis[i] == row:
            basis[i]=0
    basis[col] = row
    return (ratio, row, basis)

def new_tableau (mat, row, col, m):                      ## function 4
    for i in range (m+1):
        if i != row :
            mat = row_trans(mat, i, row, - mat[i][col]/mat[row][col])
    return mat

def check1 (mat, basis, n):                              ## function 5
    for i in range(n):
        if basis[i]==0 and mat[0][i]<0:
            return True
    return False

def check2 (mat, basis):                                 ## function 6
    score = 0
    for i in range(n):
        if basis[i]==0 and mat[0][i]==0:
            print("This LP has multiple solutions")
            score = score+1
    if score==0:
        print("The printed solution is the only solution") 

def simplex (mat, m, n, basis):                          ## function 7
    while check1(mat, basis, n):
        col = enter (mat, n)
        ratio, row, basis = leave (mat, col, m, n, basis)
        mat = new_tableau (mat, row, col, m)
    print(-mat[0][n], "is the minimum value of objective function")
    x=[]
    for i in range(n):
        if basis[i]==0:
            x.append(0)
        else:
            x.append(mat[basis[i]][n])
    print("The given minimum value occurs at the solution x = ", x) 
    return check2 (mat, basis)

## THE FINAL EXECUTION COMMAND
simplex(tableau, m, n, basis)                           ## THE FINAL EXECUTION COMMAND   


## EXPLANATION OF THE FUNCTIONS
## THE NUMBER ON STARTING REPRESENTS THE FUNCTION NUMBER IT CORRESPONDS TO

## 1. ROW TRANSFORMATION FUNCTION WITH MATRIX, ROW1, ROW2 AND A RATIO AS INPUT
## 1. OUTPUT GIVEN IS ROW1 = ROW1 + RATIO*ROW2
## 2. THE ENTERING VARIABLE FOR NEXT ITERATION IS SELECTED
## 2. SHOULD BE NEGETIVE AND WITH HIGHEST ABSOLUTE VALUE AMONGST THE NEGETIVES
## 3. LEAVING VARIABLE IS FOUND IN THIS FUNCTION USING THE RATIO TEST
## 3. IF THE CORRESPONDING CO-EFFICIENT IS NOT 1, IT IS MADE 1
## 3. THE BASIS VECTOR IS ALSO UPDATED
## 4. ROW TRANSFORMATIONS ARE MADE SUCH THAT THE CO-EFFICIENT OF ENTERING VARIABLE BECOMES ZERO IN ALL OTHER ROWS
## 4. NEW TABLEAU FOR NEXT ITERATION IS REACHED
## 5. CHECK1 ENSURES THAT ATLEAST 1 NON BASIC VARIABLE HAS A NEGETIVE CO-EFFICIENT IN THE OBJECTIVE FUNCTION
## 5. IF THIS CHECK FAILS NO FURTHER ITERATIONS WILL BE MADE
## 6. CHECK2 CHECKS FOR THE POSSIBILITY OF MULTIPLE SOLUTIONS
## 6. THE RESULT IS PRINTED WHICH TELLS IF THE L.P. HAS SINGLE SOLUTION OR MULTIPLE SOLUTIONS
## 7. FINAL SIMPLEX METHOD IS DEFINED
## 7. ITERATIONS ARE MADE WHILE CHECK1 IS TRUE
## 7. ENTERING, LEAVING AND UPDATED TABLEAU ARE DEFINED IN EACH ITERATION OF WHILE LOOP
## 7. AFTER EXITING THE LOOP, THE MINIMUM VALUE OF L.P. IS PRINTED WHICH IS NEGETIVE OF RHS OF ROW 1
## 7. USING THE BASIS VECTOR AND TABLEAU, THE VALUE OF EACH VARIABLE AT SOLUTION IS PRINTED
## 7. CHECK2 FOR MULTIPLE SOLUTIONS IS MADE
