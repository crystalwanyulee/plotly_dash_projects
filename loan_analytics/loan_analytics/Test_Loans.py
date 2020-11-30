import pytest


class Loan:
    """ Single Loan class
    With input principal, rate, payment, and extra payment, compute the amortization schedule, as well as
    overall metrics such as time to loan termination, total principal paid, and total interest paid.
    """
    def __init__(self, principal, rate, payment, extra_payment=0.0):
        """ Constructor to setup a single loan.
            :param principal:  principal amount left on the loan
            :param rate: annualized interest rate as a percentage
            :param payment: minimum expected payment
            :param extra_payment: additional payment applied to the interest
        """
        self.principal = principal
        self.rate = rate
        self.payment = payment
        self.extra_payment = extra_payment
        self.schedule = {}
        self.time_to_loan_termination = None
        self.total_principal_paid = 0.0
        self.total_interest_paid = 0.0

    def check_loan_parameters(self):
        if self.principal <= 0.0:
            raise ValueError('Principal must be greater than 0.0')
        if self.rate <= 0.0:
            raise ValueError('Rate must be greater than 0.0')
        if self.payment <= 0.0:
            raise ValueError('Payment must be greater than 0.0')
        if self.extra_payment < 0.0:
            raise ValueError('Extra payment must be greater than or equal to 0.0')

        payment_critical = self.principal * self.rate/12.0/1000.0
        if self.payment < payment_critical:
            raise ValueError(f'Payment must be greater than {payment_critical}')

    def compute_schedule(self):
        """ Compute the loan schedule.
            :return: None, the schedule is stored in an instance dictionary
        """
        begin_principal = self.principal
        payment = self.payment
        payment_number = 0

        while begin_principal > 0.0:
            payment_number += 1
            applied_interest = begin_principal * self.rate / 12.0 / 100.0
            applied_principal = payment - applied_interest + self.extra_payment
            if applied_principal > begin_principal:
                payment = begin_principal + applied_interest
                extra_payment = 0.0
                applied_principal = payment - applied_interest + extra_payment
            end_principal = begin_principal - applied_principal
            self.schedule[payment_number] = (payment_number, begin_principal, payment,
                                             self.extra_payment, applied_principal,
                                             applied_interest, end_principal)
            begin_principal = end_principal

        self.time_to_loan_termination = max(self.schedule.keys()) if len(self.schedule.keys()) > 0 else None
        self.total_interest_paid = 0.0
        self.total_principal_paid = 0.0
        for pay in self.schedule.values():
            self.total_interest_paid += pay[5]
            self.total_principal_paid += pay[4]


class LoanPortfolio:
    """ Portfolio of Loans class
    """

    def __init__(self):
        """ Constructor to setup a portfolio of loans.
        """
        self.loans = []
        self.schedule = {}

    def add_loan(self, loan):
        """ Add a loan to the portfolio
            :param loan: single loan
        """
        self.loans.append(loan)

    def remove_last_loan(self):
        """ Remove the last loan within the portfolio
        """
        self.loans.pop(-1)

    def get_loan_count(self):
        """ Return the number of loans in the portfolio
            :return: number of loans in the portfolio
        """
        return len(self.loans)

    def aggregate(self):
        """ Aggregate the loans within the portfolio by creating a schedule that includes all loans.
            :return: None, the schedule is stored in an instance dictionary
        """
        for loan in self.loans:
            for key, pay in loan.schedule.items():
                if key not in self.schedule.keys():
                    self.schedule[key] = (key, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
                begin_principal = self.schedule[key][1] + pay[1]
                payment = self.schedule[key][2] + pay[2]
                extra_payment = self.schedule[key][3] + pay[3]
                applied_principal = self.schedule[key][4] + pay[4]
                applied_interest = self.schedule[key][5] + pay[5]
                end_principal = self.schedule[key][6] + pay[6]
                self.schedule[key] = (key, begin_principal, payment, extra_payment,
                                      applied_principal, applied_interest, end_principal)

    def compute_impact(self):
        """ Compute the difference in two loans.
            :return: differences in time to loan termination and interest paid between the overall and contributor
        """
        time_to_loan_termination_all = self.loans[0].time_to_loan_termination
        total_interest_paid_all = self.loans[0].total_interest_paid

        time_to_loan_termination_contributor = self.loans[1].time_to_loan_termination
        total_interest_paid_contributor = self.loans[1].total_interest_paid

        time_to_loan_termination_diff = time_to_loan_termination_contributor - time_to_loan_termination_all
        total_interest_paid_diff = total_interest_paid_contributor - total_interest_paid_all

        time_impact = time_to_loan_termination_diff / time_to_loan_termination_contributor * 100.0
        interest_impact = total_interest_paid_diff / total_interest_paid_contributor * 100.0

        return time_to_loan_termination_diff, total_interest_paid_diff, time_impact, interest_impact


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


loans = LoanPortfolio()


@pytest.mark.parametrize('principal, rate, payment, extra_payment',
                         [
                             (5000.0, 6.0, 96.66, 0.0),
                             (10000.0, 8.0, 121.33, 0.0),
                             (7000.0, 7.0, 167.62, 0.0),
                         ])
def test_loan(principal, rate, payment, extra_payment):
    
    loan = None
    try:
        loan = compute_schedule(principal=principal, rate=rate, payment=payment, extra_payment=extra_payment)
        
    except ValueError as ex:
        print(ex)
    loans.add_loan(loan)
    

    print(round(loan.total_principal_paid, 2), round(loan.total_interest_paid, 2),
          round(loan.time_to_loan_termination, 0))

    if loans.get_loan_count() == 2:
        loans.aggregate()

    assert True


@pytest.mark.parametrize('principal, rate, payment, extra_payment, ' +
                         'total_principal_paid, total_interest_paid, time_to_loan_termination',
                         [
                             (27000.0, 4.0, 150.0, 0.0, 27000.0, 14303.0, 22 * 12.0 + 11.0),
                             (27000.0, 4.0, 150.0, 25.0, 27000.0, 10975.0, 18 * 12.0 + 2.0)
                         ])
def test_loan_with_extra_payment(principal, rate, payment, extra_payment,
                                 total_principal_paid, total_interest_paid,
                                 time_to_loan_termination):
    tolerance_for_cash = 5.0
    tolerance_for_time = 1.0

    loan = None
    try:
        loan = compute_schedule(principal=principal, rate=rate, payment=payment, extra_payment=extra_payment)
        
    except ValueError as ex:
        print(ex)
    loans.add_loan(loan)

    print(round(loan.total_principal_paid, 2), round(loan.total_interest_paid, 2),
          round(loan.time_to_loan_termination, 0))

    assert abs(loan.total_principal_paid - total_principal_paid) <= tolerance_for_cash
    assert abs(loan.total_interest_paid - total_interest_paid) <= tolerance_for_cash
    assert abs(loan.time_to_loan_termination - time_to_loan_termination) <= tolerance_for_time

    if loans.get_loan_count() == 2:
        loans.aggregate()
        
    assert True


@pytest.mark.parametrize('principal, rate, payment, extra_payment, contributions',
                         [
                             (68000.0, 4.0, 899.0, 0, [10, 100, 1000])
                         ])
def compute_loan_contribution(principal, rate, payment, extra_payment, contributions):
    loan_impacts = LoanImpacts(principal=principal, rate=rate, payment=payment,
                               extra_payment=extra_payment, contributions=contributions)
    loan_impacts.compute_impacts()

    assert True
