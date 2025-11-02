import pytest
from unittest.mock import Mock
from services.library_service import (
    pay_late_fees, refund_late_fee_payment
)
from services.payment_service import PaymentGateway

# Pay Late Fees tests

# Uses stubs to give fake valid data and a mock gateway to fake process the payment. Asserts the mock was called with valid args.
def test_succesful_payment(mocker):
    mockpaygate = Mock(spec=PaymentGateway, patron_id = "123456", amount = 1.50)
    mockpaygate.process_payment.return_value = (True, "txn_123456", "Payment of $1.5 processed successfully")
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value = {'fee_amount': 1.50,
        'days_overdue': 3})
    mocker.patch('services.library_service.get_book_by_id', return_value = {"book_id" : 1, "title" : "book"})
    success, message, trans_id = pay_late_fees("123456", 1, mockpaygate)

    assert success == True
    assert "payment successful" in message.lower()
    mockpaygate.process_payment.assert_called_with(patron_id="123456", amount=1.5, description="Late fees for 'book'")

# Uses stubs to give fake valid data, and a mock to fake the payment gateway failing. Asserts the mock was called with valid args.
def test_payment_declined_by_gateway(mocker):
    mockpaygate = Mock(spec=PaymentGateway, patron_id = "123456", amount = 1.5)
    mockpaygate.process_payment.return_value = (False, "txn_123456", "payment not successful")
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value = {'fee_amount': 1.50,
        'days_overdue': 3})
    mocker.patch('services.library_service.get_book_by_id', return_value = {"book_id" : 1, "title" : "book"})
    success, message, trans_id = pay_late_fees("123456", 1, mockpaygate)

    assert success == False
    assert "payment failed" in message.lower()
    mockpaygate.process_payment.assert_called_with(patron_id="123456", amount=1.5, description="Late fees for 'book'")

# Uses a mock gateway and asserts that the gateway wasn't called since there was an invalid id.
def test_invalid_patron_id():
    mockpaygate = Mock(spec=PaymentGateway, patron_id = "12345", amount = 1.50)
    success, message, trans_id = pay_late_fees("12345", 1, mockpaygate)

    assert success == False
    assert "invalid patron id" in message.lower()
    mockpaygate.process_payment.assert_not_called()

# Uses a stub to give 0 late fees from calculate_late_fee_for_book, and a mock gateway to check whether process_payment was called.
def test_zero_late_fees(mocker):
    mockpaygate = Mock(spec=PaymentGateway, patron_id = "123456", amount = 1.5)
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value = {'fee_amount' : 0, 'days_overdue' : 0})

    success, message, trans_id = pay_late_fees("123456", 1, mockpaygate)

    assert success == False
    assert "no late fee" in message.lower()
    mockpaygate.process_payment.assert_not_called()

# Uses stubs to give fake valid data so process_payment gets called, and the return value of process_payment was stubbed as an exception
# A Mock was used to provide the stubbed process_payment.
def test_network_error_exception_handling(mocker):
    mockpaygate = Mock(spec=PaymentGateway, patron_id = "123456", amount =1.5)
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value = {'fee_amount': 1.50,
        'days_overdue': 3})
    mocker.patch('services.library_service.get_book_by_id', return_value = {"book_id" : 1, "title" : "book"})
    mockpaygate.process_payment.return_value = Exception
    success, message, trans_id = pay_late_fees("123456", 1, mockpaygate)

    assert success == False
    assert "error" in message.lower()
    mockpaygate.process_payment.assert_called_with(patron_id="123456", amount=1.5, description="Late fees for 'book'")

# # Refund Late Fee Payment Tests

# def test_succesful_refund(mocker):


# def test_invalid_transaction_ID(mocker):


# def test_refund_amount_neg(mocker):


# def test_refund_amount_zero(mocker):


# def test_refund_amount_gt15(mocker):