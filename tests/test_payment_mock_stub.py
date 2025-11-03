import pytest
from unittest.mock import Mock
from services.library_service import (
    pay_late_fees, refund_late_fee_payment
)
from services.payment_service import PaymentGateway

# Pay Late Fees tests

# Uses stubs to give fake valid data and a mock gateway to fake process the payment. Asserts the mock was called with valid args.
def test_succesful_payment(mocker):
    mockpaygate = Mock(spec=PaymentGateway)
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
    mockpaygate = Mock(spec=PaymentGateway)
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
    mockpaygate = Mock(spec=PaymentGateway)
    success, message, trans_id = pay_late_fees("12345", 1, mockpaygate)

    assert success == False
    assert "invalid patron id" in message.lower()
    mockpaygate.process_payment.assert_not_called()

# Uses a stub to give 0 late fees from calculate_late_fee_for_book, and a mock gateway to check whether process_payment was called.
def test_zero_late_fees(mocker):
    mockpaygate = Mock(spec=PaymentGateway)
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value = {'fee_amount' : 0, 'days_overdue' : 0})

    success, message, trans_id = pay_late_fees("123456", 1, mockpaygate)

    assert success == False
    assert "no late fee" in message.lower()
    mockpaygate.process_payment.assert_not_called()

# Uses stubs to give fake valid data so process_payment gets called, and the return value of process_payment was stubbed as an exception
# A Mock was used to provide the stubbed process_payment.
def test_network_error_exception_handling(mocker):
    mockpaygate = Mock(spec=PaymentGateway)
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value = {'fee_amount': 1.50,
        'days_overdue': 3})
    mocker.patch('services.library_service.get_book_by_id', return_value = {"book_id" : 1, "title" : "book"})
    mockpaygate.process_payment.return_value = Exception
    success, message, trans_id = pay_late_fees("123456", 1, mockpaygate)

    assert success == False
    assert "error" in message.lower()
    mockpaygate.process_payment.assert_called_with(patron_id="123456", amount=1.5, description="Late fees for 'book'")

# Refund Late Fee Payment Tests

# Mocked the PaymentGateway and return_payment method call to return True, so that refund_late_fee_payment was successful.
def test_succesful_refund():
    mockpaygate = Mock(spec=PaymentGateway)
    mockpaygate.refund_payment.return_value = True, "Refund of 1.5 processed successfully. Refund ID: 123456"
    success, message = refund_late_fee_payment("txn_123456", 1.5, mockpaygate)

    assert success == True
    assert "processed successfully" in message.lower()
    mockpaygate.refund_payment.assert_called_with("txn_123456", 1.5)

# Mocked the PaymentGateway, and gave an invalid transaction id. Asserted that refund_payment wasn't called since there was an error.
def test_invalid_transaction_ID():
    mockpaygate = Mock(spec=PaymentGateway)
    success, message = refund_late_fee_payment("trans_123456", 1.5, mockpaygate)

    assert success == False
    assert "invalid transaction id" in message.lower()
    mockpaygate.refund_payment.assert_not_called()

# Mocked the PaymentGateway, and gave a neg amount. Asserted that refund_payment wasn't caalled since there was an error.
def test_refund_amount_neg():
    mockpaygate = Mock(spec=PaymentGateway)
    success, message = refund_late_fee_payment("txn_123456", -1.5, mockpaygate)

    assert success == False
    assert "amount must be greater than 0" in message.lower()
    mockpaygate.refund_payment.assert_not_called()

# Same as test_refund_amount_neg but amount is 0.
def test_refund_amount_zero():
    mockpaygate = Mock(spec=PaymentGateway)
    success, message = refund_late_fee_payment("txn_123456", 0, mockpaygate)

    assert success == False
    assert "amount must be greater than 0" in message.lower()
    mockpaygate.refund_payment.assert_not_called()

# Same as test_refund_amount_neg but amount > 15
def test_refund_amount_gt15():
    mockpaygate = Mock(spec=PaymentGateway)
    success, message = refund_late_fee_payment("txn_123456", 20.5, mockpaygate)

    assert success == False
    assert "amount exceeds maximum late fee" in message.lower()
    mockpaygate.refund_payment.assert_not_called()