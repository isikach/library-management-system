import os

import stripe

from payment_service.models import Borrowing, Payment


class PaymentService:
    FINE_MULTIPLIER = 2
    STRIPE_API_KEY = os.environ["STRIPE_API_KEY"]
    SUCCESS_URL = (
        "http://localhost:8000/api/payments/success?session_id={CHECKOUT_SESSION_ID}"
    )
    CANCEL_URL = "http://localhost:8000/api/payments/cancel/"

    @classmethod
    def create_initial_payment(cls, borrowing: Borrowing) -> None:
        borrowed_days = borrowing.expected_return_date - borrowing.borrow_date
        money_to_pay = borrowed_days.days * borrowing.book.daily_fee
        session = cls._create_stripe_session(borrowing, money_to_pay)

        Payment.objects.create(
            status="PENDING",
            payment_type="PAYMENT",
            borrowing=borrowing,
            session_url=session.url,
            session_id=session.id,
            money_to_pay=money_to_pay
        )

    @classmethod
    def create_fine_payment(cls, borrowing: Borrowing) -> None:
        overdue_days = (
            borrowing.actual_return_date - borrowing.expected_return_date
        ).days
        money_to_pay = overdue_days * borrowing.book.daily_fee * cls.FINE_MULTIPLIER
        session = cls._create_stripe_session(borrowing, money_to_pay)

        Payment.objects.create(
            status="PENDING",
            payment_type="FINE",
            borrowing=borrowing,
            session_url=session.url,
            session_id=session.id,
            money_to_pay=money_to_pay,
        )

    @classmethod
    def _create_stripe_session(cls, borrowing, money_to_pay):
        stripe.api_key = cls.STRIPE_API_KEY
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": borrowing.book.title,
                        },
                        "unit_amount": int(money_to_pay) * 100,
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=cls.SUCCESS_URL,
            cancel_url=cls.CANCEL_URL,
        )

        return session

    @classmethod
    def set_status_as_paid(cls, session_id):
        stripe.api_key = cls.STRIPE_API_KEY
        stripe.checkout.Session.retrieve(session_id)
        payment = Payment.objects.get(session_id=session_id)
        payment.status = Payment.Status.PAID
        payment.save()
