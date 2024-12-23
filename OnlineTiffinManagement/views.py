# from django.shortcuts import render,redirect
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
# from customers.models import *
# import requests
# import logging

# # Render the payment form
# def payment_form(request):
#     return render(request, 'paypal/payment_form.html')

# # Handle successful payment
# def payment_success(request):
#     # Here you can process the payment or update order status
#     return redirect(('/loggedin/'))


# # Handle payment cancellation
# def payment_cancel(request):
#     return HttpResponse("Payment Canceled. Please try again.")

# # Handle PayPal IPN (Instant Payment Notification)
# def ipn_listener(request):
#     if request.method == 'POST':
#         # Get the raw IPN message
#         ipn_message = request.body.decode('utf-8')

#         # Append 'cmd=_notify-validate' to the message and verify with PayPal
#         ipn_message += "&cmd=_notify-validate"
        
#         # Send the verification request back to PayPal
#         response = requests.post("https://ipnpb.sandbox.paypal.com/cgi-bin/webscr", data=ipn_message, headers={'Content-Type': 'application/x-www-form-urlencoded'})

#         # Process PayPal response
#         if response.text == "VERIFIED":
#             # IPN verification passed, proceed with processing the payment
#             payment_status = request.POST.get('payment_status')
#             txn_id = request.POST.get('txn_id')
#             custom_order_id = request.POST.get('custom')  # The order ID passed in the 'custom' field

#             if payment_status == "Completed":
#                 try:
#                     # Fetch the order associated with this payment
#                     order = get_object_or_404(Order, order_id=custom_order_id)

#                     # Mark the order as completed
#                     order.status = 'completed'
#                     order.transaction_id = txn_id  # Save the PayPal transaction ID
#                     order.save()

#                     # Log the successful payment processing
#                     logger.info(f"Payment successful for txn_id {txn_id}. Order {custom_order_id} processed and marked as completed.")

#                     return HttpResponse("IPN VERIFIED. Order updated.")
#                 except Order.DoesNotExist:
#                     logger.error(f"Order with ID {custom_order_id} does not exist.")
#                     return HttpResponse(f"Error: Order {custom_order_id} not found.", status=404)
#             else:
#                 # If the payment was not completed, log the status and return a response
#                 logger.warning(f"Payment not completed for txn_id {txn_id}. Payment status: {payment_status}")
#                 return HttpResponse("Payment not completed.")
#         else:
#             # If IPN verification failed
#             logger.error(f"IPN verification failed. Response from PayPal: {response.text}")
#             return HttpResponse("IPN verification failed.")
#     else:
#         # Handle invalid HTTP methods
#         logger.warning("Invalid request method for IPN listener.")
#         return HttpResponse("Invalid Request.", status=400)



import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import JsonResponse
from customers.models import order 
from customers.forms import CustomerForm
from django.contrib import messages

def create_order(request):
    form = CustomerForm(request.POST or None)
    cost = request.GET.get('cost')
    context = {
        'cost':cost,
    }
        
    
    if request.method == "POST":
    
    
        # Check if amount is provided
        amount_in_inr = request.POST.get('amount')
        
        if not amount_in_inr:
            return JsonResponse({"error": "Amount is required"}, status=400)
        
        try:
            amount_in_inr = float(amount_in_inr)  # Convert amount to float
            amount_in_paise = int(amount_in_inr * 100)  # Convert INR to paise
        except ValueError:
            return JsonResponse({"error": "Invalid amount"}, status=400)

        # Order data for Razorpay
        order_data = {
            'amount': amount_in_paise,  # Amount in paise
            'currency': 'INR',
            'payment_capture': '1',
        }

        # Initialize Razorpay client
        razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        # Create Razorpay order
        order = razorpay_client.order.create(data=order_data)
        order_id = order['id']

        context = {
            'order_id': order_id,
            'amount': amount_in_inr,  # Pass the INR amount to template for display
            'razorpay_key': settings.RAZORPAY_API_KEY,# Pass the Razorpay API Key to the template
            # 'messages': messages.get_messages(request),
            'cost': cost, 
        }

        return render(request, 'razorpay/create_order.html', context)

    # if form.is_valid():
    return render(request, 'razorpay/create_order.html',context)  # Show empty form if method is GET



from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
import razorpay
from customers.models import order  # Make sure the 'order' model is imported

def verify_payment(request):
    if request.method == 'POST':
        # Get payment details from the Razorpay response
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        amount = request.POST.get('amount')

        # Ensure the amount is received
        if not amount:
            return JsonResponse({"status": "failure", "message": "Amount not received"})

        # Initialize Razorpay client
        razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        params = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            # Verify the payment signature
            razorpay_client.utility.verify_payment_signature(params)

            # Create a new order record in the database
            new_order = order.objects.create(
                order_id=razorpay_order_id,  # Razorpay order ID
                user=request.user if request.user.is_authenticated else None,  # Associate the order with the user (if logged in)
                amount=amount,  # Set the amount paid
                status='completed',  # Mark the status as completed if payment is successful
                transaction_id=razorpay_payment_id  # Store the payment transaction ID
            )

            # Redirect to a success page after saving the order
            redirect_url = reverse('loggedin') + '?payment_successful=True'
            return redirect(redirect_url)

        except razorpay.errors.SignatureVerificationError:
            # If payment verification fails, create a new order and mark it as failed
            new_order = order.objects.create(
                order_id=razorpay_order_id,  # Razorpay order ID
                user=request.user if request.user.is_authenticated else None,  # Associate the order with the user (if logged in)
                amount=0,  # Set the amount to 0 (or adjust as per your requirement)
                status='failed',  # Mark the status as failed if payment verification fails
                transaction_id=razorpay_payment_id  # Store the payment transaction ID
            )

            # Return failure response
            return JsonResponse({"status": "failure", "message": "Payment verification failed"})

    # Return failure response if request is not POST
    return JsonResponse({"status": "failure", "message": "Invalid request method"})
