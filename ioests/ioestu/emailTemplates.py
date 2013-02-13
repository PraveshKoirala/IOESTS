rechargeSubject = 'Recharge your IOESTS balance'
rechargeMessage = '''
Dear Student,
	Your IOESTS account balance is getting low. Please recharge your account.
Thanks
'''

EMAIL_SUPERUSER = ['codegluttoners@gmail.com',]

reportSubject = "Today's Transaction Report"
reportMessage = '''
Dear Admin,
	Here is the detail report of today's transactions of IOE Student Transaction System.
'''
def getReportMessage(deposit, withdraw):
	return reportMessage + '''
	Total Deposit Amount = %d
	Total Withdraw Amount = %d
	Total Balance Transaction = %d
	Total Net Balance = %d
	''' %(deposit, withdraw, deposit + withdraw, deposit - withdraw)