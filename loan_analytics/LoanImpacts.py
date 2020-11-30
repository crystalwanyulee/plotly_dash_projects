from Loan import Loan
from LoanPortfolio import LoanPortfolio


class LoanImpacts:
    """ Contributor Impacts to Loan class
    """

    def __init__(self, principal, rate, payment, extra_payment, contributions):
        self.principal = principal
        self.rate = rate
        self.payment = payment
        self.extra_payment = extra_payment
        self.contributions = contributions
        self.results = []

    def compute_impacts(self):
        # setup a loan portfolio
        # loan_portfolio = LoanPortfolio()

        # loan with all contributions (mi)_all
        #
        loan_all = Loan(principal=self.principal, rate=self.rate,
                        payment=self.payment, extra_payment=self.extra_payment + sum(self.contributions))
        loan_all.check_loan_parameters()
        loan_all.compute_schedule()

        # loan with no contributions (mi)_0
        #
        loan_none = Loan(principal=self.principal, rate=self.rate,
                         payment=self.payment, extra_payment=self.extra_payment)
        loan_none.check_loan_parameters()
        loan_none.compute_schedule()

        micro_impact_interest_paid_all = \
            (loan_none.total_interest_paid - loan_all.total_interest_paid) / loan_all.total_interest_paid
        micro_impact_duration_all = -\
            (loan_none.time_to_loan_termination - loan_all.time_to_loan_termination) / loan_all.time_to_loan_termination

        # micro_impact_interest_paid_all = loan_none.total_interest_paid / loan_all.total_interest_paid
        # micro_impact_duration_all = loan_none.time_to_loan_termination / loan_all.time_to_loan_termination
        
        self.results.append(['Index','InterestPaid','Duration','MIInterest','MIDuration'])
        self.results.append(['All', 
                             round(loan_all.total_interest_paid, 2),
                             loan_all.time_to_loan_termination,
                             None,
                             None
                             ])
        
        self.results.append(['0', 
                             round(loan_none.total_interest_paid, 2),
                             loan_none.time_to_loan_termination,
                             round(micro_impact_interest_paid_all, 4),
                             round(micro_impact_duration_all, 4)
                             ])
        
        # iterate over each contribution (mi)_index
        #
        for index, contribution in enumerate(self.contributions):
            loan_index = Loan(principal=self.principal, rate=self.rate, payment=self.payment,
                              extra_payment=self.extra_payment + sum(self.contributions) - contribution)
            loan_index.check_loan_parameters()
            loan_index.compute_schedule()

            micro_impact_interest_paid = \
                (loan_index.total_interest_paid - loan_all.total_interest_paid) / loan_all.total_interest_paid
            micro_impact_duration = \
                (loan_index.time_to_loan_termination - loan_all.time_to_loan_termination) / loan_all.time_to_loan_termination

            # micro_impact_interest_paid = loan.total_interest_paid / loan_all.total_interest_paid
            # micro_impact_duration = loan.time_to_loan_termination / loan_all.time_to_loan_termination

            self.results.append([str(index+1), 
                                 round(loan_index.total_interest_paid, 2),
                                 loan_index.time_to_loan_termination,
                                 round(micro_impact_interest_paid, 4),
                                 round(micro_impact_duration, 4)
                                 ])
        