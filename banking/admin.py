from django.contrib import admin
from banking.models import Contact, Customer,  Operation, Updation, ATM, Transfer, Loan, ApprovedLoan, RejectedLoan, EMI

# Register your models here.
admin.site.register(Contact)
admin.site.register(Customer)
admin.site.register(Operation)
admin.site.register(Updation)
admin.site.register(ATM)
admin.site.register(Transfer)
admin.site.register(Loan)
admin.site.register(ApprovedLoan)
admin.site.register(RejectedLoan)
admin.site.register(EMI)
