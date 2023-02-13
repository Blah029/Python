class creditCard:
    """Literally the worst thing invented by mankind since pre-cracked eggs"""

    def __init__(self,customerName,bankName,accountNumber,creditLimit):
        self.cName=customerName
        self.bName=bankName
        self.account=accountNumber
        self.limit=creditLimit
        self.balance=0

    def getCustomer(self):
        """Returns the customer name"""
        return self.cName
    
    def getBank(self):
        """Returns the bank name"""
        return self.bName

    def getBalance(self):
        """Returns the account balance"""
        return "%7.2f"%self.balance

    def deposit(self,amount):
        """Proceses the transacton for a deposit of a given amount"""
        self.balance+=amount

    def witdraw(self,amount):
        """Processes the transaction for a withdrawal of a given amount"""
        
        if amount-self.balance>self.limit:
        	print("Exceeds credit limit")
        	
        else:
        	self.balance-=amount
