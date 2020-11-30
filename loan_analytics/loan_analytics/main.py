
import os
os.chdir('C://Users/admin/Documents/Python2/LoanAnalytics/loan_analytics/loan_analytics')
from Helper import *
from Loan import *
from LoanPortfolio import *
from LoanImpacts import LoanImpacts

def compute_schedule(principal, rate, payment, extra_payment):

    loan = None
    try:
        loan = Loan(principal, rate, payment, extra_payment)
        loan.check_loan_parameters()
        loan.compute_schedule()
    except ValueError as ex:
        print(ex)
        
    return loan



def compute_portfolio_schedule(loan_list):
    
    loans = LoanPortfolio()
    
    for loan in loan_list:
        loans.add_loan(loan)
    
    loans.aggregate()
    return loans



def compute_loan_contribution(principal, rate, payment, extra_payment, contributions):
    loan_impacts = LoanImpacts(principal, rate, payment, extra_payment, contributions)
    loan_impacts.compute_impacts()
    
    return loan_impacts


if __name__ == '__main__':
    compute_schedule(12000.0, 4.0, 70.0, 12.0)
    compute_schedule(5000.0, 2.0, 20.0, 6.0)
    compute_schedule(10000.0, 3.0, 60.0, 7.0)
