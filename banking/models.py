from django.db import models

class Contact(models.Model):
    firstname = models.CharField(max_length=120)
    lastname = models.CharField(max_length=120)
    email = models.EmailField(max_length=50)
    problem = models.TextField()
    date = models.DateTimeField()

    class Meta:
        db_table = "contact"

class Customer(models.Model):
    fullname = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    mobile = models.TextField(max_length=50)
    gid = models.TextField(max_length=50)
    email = models.EmailField(max_length=50)
    amount = models.FloatField()
    type = models.TextField(max_length=10)
    gender = models.TextField(max_length=20)
    date = models.DateTimeField()
    nominee = models.TextField(max_length=50)
    dob = models.TextField(max_length=15)
    class Meta:
        db_table = "customer"

class Operation(models.Model):
    mobile = models.TextField(max_length=50)
    type = models.TextField(max_length=10)
    amount = models.FloatField()
    date = models.DateTimeField()

    class Meta:
        db_table = "operation"

class Updation(models.Model):
     mobile = models.TextField(max_length=50)
     type = models.TextField(max_length=50)
     prevdata = models.TextField(max_length=50)
     newdata = models.TextField(max_length=50)
     date = models.DateTimeField()

     class Meta:
        db_table = "updation"

class ATM(models.Model):
    mobile = models.TextField(max_length=50)
    name = models.TextField(max_length=50)
    card = models.BigIntegerField()
    cvv = models.IntegerField()
    date = models.DateTimeField()

    class Meta:
        db_table = "atm"

class Transfer(models.Model):
    sender = models.TextField(max_length=50)
    receiver = models.TextField(max_length=50)
    amount = models.FloatField()
    remark = models.TextField(max_length=50)
    date = models.DateTimeField()

    class Meta:
        db_table = "transfer"

class Loan(models.Model):
    mobile = models.TextField(max_length=50)
    gid = models.TextField(max_length=50)
    amount = models.FloatField()
    purpose = models.TextField(max_length=50)
    approved = models.TextField(max_length=2)
    estatus = models.TextField(max_length=50)
    prevloan = models.TextField(max_length=50)
    returnperiod = models.IntegerField()
    income = models.IntegerField()
    remark = models.TextField(max_length=80)
    date = models.DateTimeField()

    class Meta:
        db_table = "applied_loan"

class ApprovedLoan(models.Model):
    mobile = models.TextField(max_length=50)
    gid = models.TextField(max_length=50)
    amount = models.FloatField()
    interest = models.FloatField()
    returnperiod = models.IntegerField()
    income = models.IntegerField()
    date = models.DateTimeField()
    class Meta:
        db_table = "Approved_loan"

class RejectedLoan(models.Model):
    mobile = models.TextField(max_length=50)
    gid = models.TextField(max_length=50)
    amount = models.FloatField()
    income = models.IntegerField()
    purpose = models.TextField(max_length=50)
    remark = models.TextField(max_length=50)
    date = models.DateTimeField()
    class Meta:
        db_table = "rejected_loan"

class EMI(models.Model):
    mobile = models.TextField(max_length=50)
    gid = models.TextField(max_length=50)
    returnperiod = models.IntegerField()
    returned = models.IntegerField()
    emi = models.FloatField()
    class Meta:
        db_table = "emi_payment"



