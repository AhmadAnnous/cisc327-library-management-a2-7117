import pytest
from unittest.mock import Mock
from services.library_service import (
    pay_late_fees, refund_late_fee_payment
)
from services.payment_service import PaymentGateway

# Pay Late Fees tests
def test_succesful_payment(mocker):
    mockpaygate = Mock(spec=PaymentGateway, patron_id = "123456", amount = 1.50)
    mockpaygate.process_payment.return_value = (True, "txn_123456", "Payment of $1.5 processed successfully")
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value = {'fee_amount': 1.50,
        'days_overdue': 3})
    mocker.patch('services.library_service.get_book_by_id', return_value = {"book_id" : 1, "title" : "book"})
    success, message, trans_id = pay_late_fees("123456", 1, mockpaygate)

    assert success == True
    assert "payment successful" in message.lower()
    mockpaygate.process_payment.assert_called_once()

# def test_payment_declined_gateway(mocker):


# def test_invalid_patron_id(mocker):


# def test_zero_late_fees(mocker):


# def test_network_error_exception_handling(mocker):



# # Refund Late Fee Payment Tests

# def test_succesful_refund(mocker):


# def test_invalid_transaction_ID(mocker):


# def test_refund_amount_neg(mocker):


# def test_refund_amount_zero(mocker):


# def test_refund_amount_gt15(mocker):