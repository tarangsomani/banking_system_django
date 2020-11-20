# banking_system_django

APIs - 

       account -- CustomerSignUpView
                  LoginView
                  CustomerDepositAmountView
                  CustomerWithdrawAmountView
                  CustomerAccountDetailsView
       
     - bank_manager -- GetTransactionHistoryView (returns a CSV for the filtered records)


ThirdParty - 

     - Using Sendgrid to send emails for transactions to Users (Customers)


Postman Collection: https://www.getpostman.com/collections/474a36dcdb2778370e40


Run All Tests -
          
          pytest
