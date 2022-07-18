from logging.config import valid_ident
from unittest import mock
from django.shortcuts import redirect, render, HttpResponse
from datetime import datetime
from banking.models import Contact, Customer,  Operation, Updation, ATM, Transfer, Loan, ApprovedLoan, RejectedLoan, EMI
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.conf import settings
from django.core.mail import send_mail
from random import randint

def index(request):
    return render(request, 'frontpage.html')
def aboutus(request):
    return render(request, 'aboutus.html')

def contact(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        problem = request.POST.get('problem')
        contact = Contact(firstname=firstname,lastname=lastname, email=email, problem = problem, date = datetime.today())
        contact.save()
        print(firstname)
    return render(request, 'contact.html')


def register(request):
	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['username']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		email = request.POST['email']

		if password1 == password2:
			if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
				messages.info(request,'Username or email already taken')
				return redirect('register')

			else:
				user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
				user.save()
				return redirect('login')
	else:
		return render(request, 'register.html')


def login(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username,password=password)

		if user is not None:
			auth.login(request, user)
			return redirect('/')

		else:
			messages.info(request, 'Invalid credentials')
			return redirect('login')
	else:
		return render(request, 'login.html')


def logout(request):
	auth.logout(request)
	return redirect('/')


@login_required()
def customer(request):
	if request.method == "POST":
		fullname = request.POST.get('fullname')
		address = request.POST.get('address')
		mobile = request.POST.get('mobile')
		gid = request.POST.get('gid')  
		email = request.POST.get('email')
		amount = request.POST.get('amount')
		type = request.POST.get('type')
		gender = request.POST.get('gender')
		nominee = request.POST.get('nominee')
		dob = request.POST.get('dob')

		if Customer.objects.filter(mobile=mobile) or Customer.objects.filter(email=email) or Customer.objects.filter(gid=gid):
			messages.error(request, 'some of your data is matching with our record')
		else:
			customer = Customer(fullname=fullname, address=address, mobile=mobile,gid=gid, email=email, amount=amount, type=type, gender=gender,nominee=nominee, dob=dob, date=datetime.today())
			customer.save()
			subject = 'welcome to AV Banking solution.'
			message = f'Hi {fullname},thank you for chosing us. Your account has been created successfully.\n With following details\n a/c:- {mobile} \n id proof no:- {gid} \n address:- {address} \n initial balance:- {amount} \n Date of birth:- {dob}\n Nominee name:- {nominee}\n\nFeel free to contact us.\n THANK YOU.'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [email]
			send_mail( subject, message, email_from, recipient_list )
			messages.success(request, 'account created successfully')
	
	return render(request, 'customer.html')


@login_required()
def operation(request):
	if request.method == "POST":
		mobile = request.POST.get('mobile')
		amount = float(request.POST.get('amount'))
		type = request.POST.get('type')
		gid = request.POST.get('gid')
		if Customer.objects.filter(mobile=mobile, gid=gid):
			cust = Customer.objects.get(mobile=mobile)
			bal = float(cust.amount)
			if type=="withdrawl":
				if amount>bal:
					messages.error(request, 'Not enough balance')
				else:
					cust.amount = bal - amount
					cust.save()
					print('balance withdrawn')
					messages.success(request, 'Balance withdrawn successfully')
			
			if type=="deposit":
				cust.amount = bal + amount
				cust.save()
				print('balance updated')
				messages.success(request, 'balance deposited successfully')
		else:
			messages.error(request, 'Provide correct information')
		
		operation = Operation(mobile=mobile, amount=amount, type=type, date=datetime.today())
		operation.save()

	return render(request, 'operation.html')

@login_required()
def update(request):
	if request.method == "POST":
		mobile = request.POST.get('mobile')
		gid = request.POST.get('gid')
		choose = request.POST.get('choose')
		update = request.POST.get('update')
		
		if Customer.objects.filter(mobile=mobile, gid=gid):
			cust = Customer.objects.get(mobile=mobile)
			if choose=="email":
				if Customer.objects.filter(email=update):
					messages.error(request, 'Data already exists! Provide correct data')
				else:
					up = Updation(mobile=mobile, type=choose, prevdata = cust.email, newdata= update, date=datetime.today())
					up.save()
					cust.email = update
					cust.save()
					messages.success(request, "email updated successfully")
			elif choose=="fullname":
				up = Updation(mobile=mobile, type=choose, prevdata = cust.fullname, newdata= update, date=datetime.today())
				up.save()
				cust.fullname = update
				cust.save()
				messages.success(request, "full name updated successfully")
			elif choose=="address":
				up = Updation(mobile=mobile, type=choose, prevdata = cust.address, newdata= update, date=datetime.today())
				up.save()
				cust.address = update
				cust.save()
				messages.success(request, "Addresss updated successfully")
			elif choose=="nominee":
				up = Updation(mobile=mobile, type=choose, prevdata = cust.nominee, newdata= update, date=datetime.today())
				up.save()
				cust.nominee = update
				cust.save()
				messages.success(request, "Nominee name updated successfully")

		else:
			messages.error(request, "Provide correct information")

	return render(request, 'update.html')

@login_required()
def delete(request):
	if request.method == "POST":
		mobile = request.POST.get('mobile')
		gid = request.POST.get('gid')
		if Customer.objects.filter(mobile=mobile, gid=gid):
			cust = Customer.objects.get(mobile=mobile)
			bal = float(cust.amount)
			print(bal)
			if bal > 2 or ApprovedLoan.objects.filter(mobile=mobile):
				messages.error(request, "Clear all loan/withdraw all amount")
			else:
				update = Updation(mobile=mobile, type="delete", prevdata = cust.mobile, newdata= "0", date=datetime.today())
				update.save()
				cust.delete()
				messages.success(request, "Your account deleted successfully")
		else:
			messages.error(request, "Provide correct information")

	return render(request, 'delete.html')

@login_required()
def trans(request):
	txn = Operation.objects.all()
	return render(request, 'transaction.html', {'txn': txn})

@login_required()
def atm(request):
	if request.method == "POST":
		mobile = request.POST.get('mobile')
		gid = request.POST.get('gid')
		if Customer.objects.filter(mobile=mobile, gid=gid):
			cust = Customer.objects.get(mobile=mobile)
			cvv = randint(100,999)
			card = randint(3234567891021025, 9878545874102357)
			while ATM.objects.filter(card = card):
				card = randint(16)
			if ATM.objects.filter(mobile = mobile):
				messages.error(request, "Already have an active card")
			else:
				atm = ATM(mobile=mobile, name=cust.fullname, card=card, cvv =cvv, date=datetime.today())
				atm.save()
				subject = 'welcome to AV Banking solution.'
				message = f'Hi {cust.fullname},Aplliaction for new card has been processed successfully.It will dispatch within next three working days.\n Card details:-\n a/c:- {mobile} \n Name on card:- {cust.fullname}\n card no. :- {card} \n cvv no. :- {cvv}\n date applied :- {datetime.today()} \n \nExpiry date:- 4 years from date applied\n\n THANK YOU.'
				email_from = settings.EMAIL_HOST_USER
				recipient_list = [cust.email]
				send_mail( subject, message, email_from, recipient_list )		
				messages.success(request, "Applied for card successfully.")

		else:
			messages.error(request, "Provide correct information")


	return render(request, 'atm.html')


@login_required()
def transfer(request):
	if request.method == "POST":
		sender = request.POST.get('sender')
		receiver = request.POST.get('receiver')
		gid = request.POST.get('gid')
		remark = request.POST.get('remark')
		amount = float(request.POST.get('amount'))
		if Customer.objects.filter(mobile=sender, gid=gid) and Customer.objects.filter(mobile=receiver) and sender != receiver:
			c1 = Customer.objects.get(mobile = sender)
			c2 = Customer.objects.get(mobile = receiver)
			c1amount = float(c1.amount)
			c2amount = float(c2.amount)
			if amount > c1amount:
				messages.error(request, "Balance is insufficient")
			else:
				c1.amount = c1amount - amount
				c2.amount = c2amount + amount
				c1.save()
				c2.save()
				tfr = Transfer(sender=sender, receiver=receiver, amount=amount, remark=remark, date= datetime.today())
				tfr.save()
				messages.success(request, "Balance transferred successfully")
		else:
			messages.error(request, "Recheck the data and provide again.")
	return render(request, 'customertocustomer.html')

@login_required()
def applyforloan(request):
	if request.method == "POST":
		mobile = request.POST.get('mobile')
		gid = request.POST.get('gid')
		amount = request.POST.get('amount')
		purpose = request.POST.get('purpose')
		estatus = request.POST.get('status')
		prevloan = request.POST.get('prevloan')
		returnperiod = request.POST.get('returnperiod')
		income = request.POST.get('income')
		if Customer.objects.filter(mobile=mobile, gid=gid):
			if Loan.objects.filter(mobile = mobile, approved ="0") or ApprovedLoan.objects.filter(mobile=mobile):
				messages.error(request, "One loan application is still pending/approved")
			else:
				loan = Loan(mobile=mobile, gid=gid, amount=amount, purpose=purpose,estatus=estatus,returnperiod=returnperiod, income=income, prevloan=prevloan,approved="0",remark="none", date=datetime.today())
				loan.save()
				messages.success(request, "Successfully applied for loan, Check mail for confirmation.")
		else:
			messages.error(request, "Recheck the data and provide again.")
	return render(request, 'applyforloan.html')

@login_required()
def viewcustomer(request):
	if request.method == "POST":
		mobile = request.POST.get('mobile')
		gid = request.POST.get('gid')
		if Customer.objects.filter(mobile=mobile, gid=gid):
			try:
				cust = Customer.objects.get(mobile=mobile)
				opern = Operation.objects.filter(mobile=mobile)
				tfr1 = Transfer.objects.filter(sender=mobile)
				tfr2 = Transfer.objects.filter(receiver=mobile)
				up = Updation.objects.filter(mobile=mobile)
				al = ApprovedLoan.objects.get(mobile=mobile)
				
			except:
				opern = None
				tfr1 = None
				tfr2 = None
				up = None
				al = None
			return render(request, 'viewcustomer.html',{'cust': cust, 'opern':opern, 'tfr1':tfr1, 'tfr2':tfr2, 'up':up, 'al':al})
		else:
			messages.error(request, "Provide correct information or no txn available for customer")
	return render(request, 'sortedcustomer.html')

@login_required()
def loanapproval(request):
	if request.method == "POST":
		account = request.POST.get('account')
		approved = request.POST.get('approved')
		interest = request.POST.get('interest')
		remark = request.POST.get('remark')
		cust = Customer.objects.get(mobile = account)
		ldata = Loan.objects.get(mobile = account)
		if approved == "yes":
			lapprove = ApprovedLoan(mobile = account, amount = ldata.amount, gid = cust.gid, interest = interest, returnperiod=ldata.returnperiod, income = ldata.income, date = datetime.today())
			lapprove.save()
			ldata.approved = "1"
			ldata.remark = remark
			ldata.save()
			subject = 'AV BANKING. Loan related information.'
			message = f'Hi {cust.fullname},Congrats, Your loan application has been accepted.\nLoan amount:- {ldata.amount}\nInterest:-{interest}\nReturn period:- {ldata.returnperiod} months\nFor further information contact bank.\n\nTHANK YOU.'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [cust.email]
			send_mail( subject, message, email_from, recipient_list )		
			messages.success(request, "Loan application accepted.")

			p = float(ldata.amount)
			t = float(ldata.returnperiod)
			r = float(interest)
			inte = float((p*t*r)/100)
			amnt = float(p+inte)
			emip = float(amnt/t)
			emisave = EMI(mobile = cust.mobile, gid = cust.gid, returnperiod = ldata.returnperiod, returned = 0, emi = emip)
			emisave.save()
		else:
			rloan = RejectedLoan(mobile = account, gid = cust.gid, amount=ldata.amount,income = ldata.income, purpose = ldata.purpose, remark = remark,date = datetime.today())
			rloan.save()
			ldata.delete()
			subject = 'Rejection of your loan application.'
			message = f'Hi {cust.fullname}, Sorry to say that you loan application has been rejected.\n If you wish please apply agin with more details.\nFor further information contact branch\n\nTHANK YOU.'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [cust.email]
			send_mail( subject, message, email_from, recipient_list )

			messages.error(request,"Loan rejected apply fresh application")
	loan = Loan.objects.filter(approved="0")
	return render(request, 'approvalforloan.html', {'loan':loan})

@login_required()
def viewtransfer(request):
	tfr = Transfer.objects.all()
	return render(request, 'viewtransfer.html', {'tfr':tfr})

@login_required()
def atmcard(request):
	atm = ATM.objects.all()
	return render(request, 'atmcard.html', {'atm':atm})

@login_required()
def emiview(request):
	if request.method == "POST":
		mobile = request.POST.get('mobile')
		gid = request.POST.get('gid')
		if EMI.objects.filter(mobile=mobile, gid=gid):
			emi = EMI.objects.get(mobile=mobile)
			global val
			def val():
				return emi
			return redirect('emi')
		else:
			messages.error(request, "Provide correct information")

	return render(request, 'emipayment.html')

@login_required()
def emi(request):
	emipay = val()
	if request.method == "POST":
		
		print(emipay.mobile)
		returned = int(emipay.returned)
		returnperiod = int(emipay.returnperiod)
		print(returned)
		if returned < returnperiod:
			retun = returned+1
			print(retun)
			emipay.returned = retun
			emipay.save()
			messages.success(request, "EMI PAYMENT DONE SUCCESSFULLY.")
			return redirect('emiview')
		else:
			messages.error(request, "Provide correct information")

	
	return render(request, 'emipayment2.html', {'emi':emipay})

