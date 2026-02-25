import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import InitiateTransactionSerializer
from .mtn_client import MTNMoMoClient
from .airtel_client import AirtelMoneyClient
from .models import MobileMoneyTransaction


class InitiateTransactionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = InitiateTransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        telecom = data['telecom']
        transaction_type = data['transaction_type']
        amount = data.get('amount', 0)
        recipient_phone = data.get('recipient_phone', '')
        session_id = data.get('session_id', str(uuid.uuid4()))

        transaction = MobileMoneyTransaction.objects.create(
            session_id=session_id,
            transaction_type=transaction_type,
            amount=amount,
            recipient_phone=recipient_phone,
            telecom=telecom,
            status='pending',
        )

        reference = str(uuid.uuid4())
        if telecom == 'MTN':
            client = MTNMoMoClient()
            result = client.request_to_pay(float(amount), 'UGX', recipient_phone, reference, 'SautiAgent payment')
        else:
            client = AirtelMoneyClient()
            result = client.request_payment(float(amount), 'UGX', recipient_phone, reference)

        if result.get('status') == 'pending':
            ref_id = result.get('reference_id') or result.get('transaction_id', reference)
            transaction.telecom_reference = ref_id
            transaction.save()
            return Response({'success': True, 'data': {
                'status': 'pending',
                'reference_id': ref_id,
                'message': 'Please enter your PIN on your phone',
            }})
        else:
            transaction.status = 'failed'
            transaction.save()
            return Response({'success': False, 'error': result.get('error', 'Transaction failed'), 'code': 'TRANSACTION_FAILED'}, status=status.HTTP_502_BAD_GATEWAY)


class TransactionStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, reference_id):
        try:
            transaction = MobileMoneyTransaction.objects.get(telecom_reference=reference_id)
        except MobileMoneyTransaction.DoesNotExist:
            return Response({'success': False, 'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)

        if transaction.telecom == 'MTN':
            client = MTNMoMoClient()
            result = client.get_transaction_status(reference_id)
        else:
            client = AirtelMoneyClient()
            result = client.get_transaction_status(reference_id)

        if 'error' not in result:
            transaction.status = result.get('status', 'pending')
            transaction.save()

        return Response({'success': True, 'data': result})
