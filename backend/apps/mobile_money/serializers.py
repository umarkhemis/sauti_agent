from rest_framework import serializers


class InitiateTransactionSerializer(serializers.Serializer):
    telecom = serializers.ChoiceField(choices=['MTN', 'AIRTEL'])
    transaction_type = serializers.ChoiceField(choices=['send', 'receive', 'balance', 'airtime', 'data', 'loan'])
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    recipient_phone = serializers.CharField(max_length=20, required=False, default='')
    session_id = serializers.CharField(required=False, default='')


class TransactionStatusSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField(allow_null=True, required=False)
    reference_id = serializers.CharField(required=False)
