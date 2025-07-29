from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import *
from .serializer import QBarDetailsSerializer
import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
   
class AddQBarDetails(APIView):
    def post(self, request):
        today_date = datetime.date.today()
        current_year = today_date.year
        current_month = today_date.month
        fm = f"{current_year}{today_date.strftime('%m')}"

        # Determine financial year
        if current_month < 4:
            fy = f"{current_year - 1}-{current_year}"
        else:
            fy = f"{current_year}-{current_year + 1}"

        is_qrcode_downloaded = request.data.get('is_qrcode_downloaded', False)
        is_barcode_downloaded = request.data.get('is_barcode_downloaded', False)

        try:
            qbar = QBarDetails.objects.get(user=None)
            # Update existing entry
            if is_qrcode_downloaded:
                request.data['qrcode_download_count'] = qbar.qrcode_download_count + 1
            elif is_barcode_downloaded:
                request.data['barcode_download_count'] = qbar.barcode_download_count + 1
            else:
                request.data['view_count'] = qbar.view_count + 1

            serializer = QBarDetailsSerializer(qbar, data=request.data, partial=True)
        except QBarDetails.DoesNotExist:
            # No entry exists, create new
            if is_qrcode_downloaded:
                request.data['qrcode_download_count'] = 1
            elif is_barcode_downloaded:
                request.data['barcode_download_count'] = 1
            else:
                request.data['view_count'] = 1

            serializer = QBarDetailsSerializer(data=request.data, partial=True)

        # Save the serializer
        if serializer.is_valid():
            serializer.save(
                financial_year=fy,
                month=fm,
                current_year=current_year,
                latest_created_at=timezone.now()
            )
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            print("Validation Error:", serializer.errors)
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class SendEmail(APIView):
    def post(self, request):
        # Hardcoded recipient (admin)
        recipient_email = "atozdigisol@gmail.com"

        # Get form data from request
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        email_address = request.data.get("email_address", '')
        message = request.data.get("message", '')
        is_aggree = request.data.get("is_aggree", '')

        try:
            # Subject
            email_subject = f'📩 QBar Gen | Contact Form Submission from {first_name} {last_name}'

            # Render HTML body from template
            email_html_body = render_to_string('contact_email.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email_address': email_address,
                'message': message,
                'is_aggree': is_aggree,
            })

            # Compose email
            email = EmailMessage(
                subject=email_subject,
                body=email_html_body,
                from_email="QBar <no-reply@yourdomain.com>",
                to=[recipient_email],
            )
            email.content_subtype = 'html'  # Send as HTML
            email.send()

            return Response({"status": "success"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     