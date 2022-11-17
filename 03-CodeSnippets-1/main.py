def fnRemoveTrailingZero():
	print('Removing trailing zero after decimal point')
	a = input('Key in a number (decimal or integer). Any unnecessary zeros will be removed:')
	a = str(a)
	a= a.rstrip('0').rstrip('.') if '.' in a else a
	print('Compact number is: {}'.format(a))

def fnShowSnippetList():
	iNo = 0
	print('List of the snippets')
	print('1. Removing trailing zero after a decimal point')
	iNo = int(input('Which snippet is to run (0 to exit):'))
	return iNo
	
bRun = True
while bRun:
	iNo = fnShowSnippetList()
	if iNo == 0:
		bRun = False
	elif iNo == 1:
		fnRemoveTrailingZero()