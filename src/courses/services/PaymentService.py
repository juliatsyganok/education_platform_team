from ..exceptions import PaymentFailedError, InsufficientFundsError
class PaymentService:
    @staticmethod
    def make_a_payment(cost, user_balance=None):
        if user_balance is not None and user_balance<cost:
            raise InsufficientFundsError()
        success=True
        if not success:
            raise PaymentFailedError
        return True
