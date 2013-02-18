rechargeSubject = 'Recharge your IOESTS balance'
rechargeMessage = '''
Dear Student,
	Your IOESTS account balance is getting low. Please recharge your account.
Thanks
'''


resetSubject = "Automatic IOESTS Mail Engine"
def getResetMessage(username, userid, link, salt):
	resetMessage = '''
Dear %s,
	This mail is from the IOESTS for the reset of password of the student ID %s. You can reset your password by clicking on the link below.
http://127.0.0.1:8000/resetPassword/%s%sU%s
For further information please contact admin. 
Thanks
'''% (username, userid, salt, link, userid)
	return resetMessage


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