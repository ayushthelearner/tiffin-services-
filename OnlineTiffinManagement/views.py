from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from customers.models import *
import requests
import logging

# Render the payment form
def payment_form(request):
    return render(request, 'paypal/payment_form.html')

# Handle successful payment
def payment_success(request):
    # Here you can process the payment or update order status
    return redirect(('/loggedin/'))


# Handle payment cancellation
def payment_cancel(request):
    return HttpResponse("Payment Canceled. Please try again.")

# Handle PayPal IPN (Instant Payment Notification)
def ipn_listener(request):
    if request.method == 'POST':
        # Get the raw IPN message
        ipn_message = request.body.decode('utf-8')

        # Append 'cmd=_notify-validate' to the message and verify with PayPal
        ipn_message += "&cmd=_notify-validate"
        
        # Send the verification request back to PayPal
        response = requests.post("https://ipnpb.sandbox.paypal.com/cgi-bin/webscr", data=ipn_message, headers={'Content-Type': 'application/x-www-form-urlencoded'})

        # Process PayPal response
        if response.text == "VERIFIED":
            # IPN verification passed, proceed with processing the payment
            payment_status = request.POST.get('payment_status')
            txn_id = request.POST.get('txn_id')
            custom_order_id = request.POST.get('custom')  # The order ID passed in the 'custom' field

            if payment_status == "Completed":
                try:
                    # Fetch the order associated with this payment
                    order = get_object_or_404(Order, order_id=custom_order_id)

                    # Mark the order as completed
                    order.status = 'completed'
                    order.transaction_id = txn_id  # Save the PayPal transaction ID
                    order.save()

                    # Log the successful payment processing
                    logger.info(f"Payment successful for txn_id {txn_id}. Order {custom_order_id} processed and marked as completed.")

                    return HttpResponse("IPN VERIFIED. Order updated.")
                except Order.DoesNotExist:
                    logger.error(f"Order with ID {custom_order_id} does not exist.")
                    return HttpResponse(f"Error: Order {custom_order_id} not found.", status=404)
            else:
                # If the payment was not completed, log the status and return a response
                logger.warning(f"Payment not completed for txn_id {txn_id}. Payment status: {payment_status}")
                return HttpResponse("Payment not completed.")
        else:
            # If IPN verification failed
            logger.error(f"IPN verification failed. Response from PayPal: {response.text}")
            return HttpResponse("IPN verification failed.")
    else:
        # Handle invalid HTTP methods
        logger.warning("Invalid request method for IPN listener.")
        return HttpResponse("Invalid Request.", status=400)





