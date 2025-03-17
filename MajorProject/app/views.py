from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from .models import CustomUser, Trek, Booking, Discount
from django.utils.timezone import now
import random
from django.db.models import Sum, Count
import json
from datetime import datetime
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from .form import SignupForm, ResetPasswordForm
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse, JsonResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
import logging
logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'landing.html') 

def generate_otp():
    return str(random.randint(100000, 999999))

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # Keep user inactive until OTP verification
            
            # Generate OTP and save it to the database
            otp = generate_otp()
            user.otp = otp
            user.save()

            # Send OTP email
            subject = "Your OTP for Email Verification"
            html_message = render_to_string(
                'otp_email.html',
                {
                    'user': user,
                    'otp': otp,
                    'current_year': datetime.now().year
                }
            )
            email = EmailMessage(
                subject=subject,
                body=html_message,
                from_email='your-email@example.com',  # Replace with your sender email
                to=[user.email],
            )
            email.content_subtype = "html"
            email.send()

            return redirect(reverse('verify_otp', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk))}))
        else:
            messages.error(request, "Invalid form submission. Please check your inputs.")

    else:
        form = SignupForm()

    return render(request, 'register.html', {'form': form})

def verify_otp(request, uidb64):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)

        if user.otp == otp_entered:  # Check OTP from database
            user.is_active = True
            user.is_verified = True
            user.otp = None  # Clear OTP after verification
            user.save()

            # Send a thank-you email after successful verification
            subject = "Thank You for Verifying Your Email!"
            html_message = render_to_string(
                'thank_you_email.html',
                {
                    'user': user,
                    'current_year': datetime.now().year
                }
            )
            email = EmailMessage(
                subject=subject,
                body=html_message,
                from_email='your-email@example.com',  # Replace with your sender email
                to=[user.email],
            )
            email.content_subtype = "html"
            email.send()

            messages.success(request, "Account verified successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'verify_otp.html', {'uidb64': uidb64})

def resend_otp(request, uidb64):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = get_user_model().objects.get(pk=uid)
    
    # Generate a new OTP and save it
    otp = generate_otp()
    user.otp = otp
    user.save()
    
    # Prepare OTP email
    subject = "Your OTP for Email Verification"
    html_message = render_to_string(
        'otp_email.html', 
        {
            'user': user,
            'otp': otp,
            'current_year': datetime.now().year
        }
    )
    email = EmailMessage(
        subject=subject,
        body=html_message,
        from_email='your-email@example.com',  # Replace with your sender email
        to=[user.email],
    )
    email.content_subtype = "html"
    email.send()

    return redirect(reverse('verify_otp', kwargs={'uidb64': uidb64}))

def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user_obj = CustomUser.objects.get(email=email)  # Get the user object using email
            user = authenticate(request, username=user_obj.username, password=password)  # Use username, not email
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, "login.html", {"error": True})

    return render(request, "login.html")


# Utility function to send OTP email with inline CSS
def send_forgot_password_otp(email):
    otp = random.randint(100000, 999999)  # Generate a random 6-digit OTP
    subject = 'OTP Verification for Password Reset Request'

    # Professional email body with inline CSS
    message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333; padding: 20px; background-color: #f4f4f4;">
                <table role="presentation" style="width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; padding: 20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <tr>
                        <td style="text-align: center; font-size: 24px; font-weight: bold; padding-bottom: 20px; color: #00b4db;">
                            Password Reset Request
                        </td>
                    </tr>
                    <tr>
                        <td style="font-size: 16px; line-height: 1.6; padding-bottom: 20px;">
                            <p>Dear User,</p>
                            <p>We have received a request to reset your password for your account on <strong>Sahyadri Trails</strong>. To proceed with the password reset, please enter the One-Time Password (OTP) provided below:</p>
                            <p style="font-size: 24px; font-weight: bold; color: #0083b0; text-align: center;">OTP: {otp}</p> <!-- Centered OTP -->
                            <p>This OTP is valid for 10 minutes.</p>
                            <p>For security reasons, please do not share this OTP with anyone. If you did not request a password reset, please disregard this email, and your account will remain secure.</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="text-align: center; padding-top: 20px; font-size: 14px; color: #666;">
                            <p>If you have any questions or need further assistance, feel free to contact us at <strong>sahyadritrails@gmail.com</strong>.</p>
                            <p style="font-weight: bold;">Best regards,</p>
                            <p><strong>Sahyadri Trails Support Team</strong></p>
                        </td>
                    </tr>
                </table>
            </body>
        </html>
        """


    # Send email with the subject and formatted message
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], html_message=message)
    
    return otp

# Forgot Password View (Enter email)
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if CustomUser.objects.filter(email=email).exists():
            otp = send_forgot_password_otp(email)
            request.session['forgot_password_otp'] = otp
            request.session['forgot_password_email'] = email
            return redirect('verify_otp')  # Redirect to OTP verification page
        else:
            messages.error(request, "Email not registered.")
    return render(request, 'forgot_password.html')

# OTP Verification View
def verify_forgot_password_otp(request):
    if request.method == "POST":
        otp_input = request.POST.get('otp')
        email = request.session.get('forgot_password_email')
        otp = request.session.get('forgot_password_otp')

        if otp_input == str(otp):
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify_otp')
    return render(request, 'verify_forgot_password_otp.html')

# Resend OTP View
def resend_forgot_password_otp(request):
    email = request.session.get('forgot_password_email')
    if email:
        otp = send_forgot_password_otp(email)
        request.session['forgot_password_otp'] = otp
        messages.success(request, "OTP resent successfully.")
        return redirect('verify_otp')
    else:
        return redirect('forgot_password')

def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            email = request.session.get('forgot_password_email')
            
            # Fetch user by email using filter, not get
            users = CustomUser.objects.filter(email=email)
            
            if users.count() == 1:
                user = users.first()
                user.set_password(password)
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect('login')
            else:
                messages.error(request, "Error: Multiple users found with this email. Please contact support.")
                return redirect('forgot_password')
    else:
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')


def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST['username']
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone_number = request.POST['phone']

        # Check if the new username already exists (excluding the current user)
        if CustomUser.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, "Username is already taken. Please choose another.")
            return redirect('profile')

        # Check if the new email already exists (excluding the current user)
        if CustomUser.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, "Email is already registered. Please use another.")
            return redirect('profile')

        # Split full_name into first_name and last_name safely
        name_parts = full_name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Update user details
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone = phone_number  # Ensure your CustomUser model has a `phone` field

        try:
            user.save()
            messages.success(request, "Profile updated successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('profile')

    return render(request, 'profile.html')


def explore_treks(request):
    query = request.GET.get("q", "")  # Get search term
    if query:
        treks = Trek.objects.filter(name__icontains=query)  # Case-insensitive search
    else:
        treks = Trek.objects.all()
    return render(request, 'explore.html', {'treks': treks})

def contact(request):
    return render(request, 'contact.html')


def bookings_page(request):
    treks = Trek.objects.all()  # Fetching all treks
    
    paginator = Paginator(treks, 6)  # Show 6 treks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'bookings.html', {'treks': page_obj})  # ✅ Pass paginated data

@login_required
def create_booking(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        trek_id = request.POST.get('trek_id')

        if not trek_id:
            return JsonResponse({"success": False, "error": "Trek ID is missing!"}, status=400)

        try:
            trek_id = int(trek_id)  # ✅ Ensure trek_id is an integer
            trek = get_object_or_404(Trek, trek_id=trek_id)  # ✅ Check if trek exists
            date = request.POST.get('date')
            number_of_people = int(request.POST.get('number_of_people', 1))
            total_price = trek.price * number_of_people  

            # ✅ Match field names in the Booking model
            booking = Booking.objects.create(
                trek=trek,
                name=request.user.username,  # ✅ Match `name` field
                email=request.user.email,  # ✅ Keep email
                date=date,  # ✅ Keep date
                number_of_people=number_of_people,  # ✅ Keep number_of_people
                total_price=total_price  # ✅ Keep total_price
            )

            return JsonResponse({"success": True, "message": f"Booking successful for {trek.name}!"})

        except ValueError:
            return JsonResponse({"success": False, "error": "Invalid trek ID format!"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)

def booking_details(request):
    bookings = Booking.objects.filter(email=request.user.email)
    return render(request, 'bookingdetails.html', {'bookings': bookings}) 

def download_booking_pdf(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Booking_{booking.id}.pdf"'

    # Create PDF Document
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    # Custom styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Title'], fontSize=18, textColor=colors.darkblue)
    section_title_style = ParagraphStyle('SectionTitle', parent=styles['Heading2'], fontSize=14, textColor=colors.blueviolet)
    normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontSize=12, leading=18)
    bold_style = ParagraphStyle('BoldStyle', parent=styles['Normal'], fontSize=12, leading=18, fontName='Helvetica-Bold')

    # Add a header
    elements.append(Paragraph("Booking Confirmation", title_style))
    elements.append(Spacer(1, 10))

    # Add a logo (Optional)
    # try:
    #     logo_path = "static/images/logo.png"  # Adjust the path
    #     logo = Image(logo_path, width=100, height=50)
    #     elements.append(logo)
    # except:
    #     pass  # Skip if the logo isn't found

    elements.append(Spacer(1, 20))

    # Booking Details Section
    elements.append(Paragraph("Booking Details", section_title_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"<b>Name:</b> {booking.name}", normal_style))
    elements.append(Paragraph(f"<b>Email:</b> {booking.email}", normal_style))
    elements.append(Paragraph(f"<b>Date:</b> {booking.date.strftime('%Y-%m-%d')}", normal_style))
    elements.append(Paragraph(f"<b>Number of People:</b> {booking.number_of_people}", normal_style))
    elements.append(Paragraph(f"<b>Total Price:</b> Rs.{booking.total_price}", normal_style))

    elements.append(Spacer(1, 20))

    # Trek Details Section
    elements.append(Paragraph("Trek Details", section_title_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"<b>Trek Name:</b> {booking.trek.name}", normal_style))
    elements.append(Paragraph(f"<b>Difficulty:</b> {booking.trek.difficulty}", normal_style))
    elements.append(Paragraph(f"<b>Season:</b> {booking.trek.season}", normal_style))
    elements.append(Paragraph(f"<b>Duration:</b> {booking.trek.duration} days", normal_style))
    elements.append(Paragraph(f"<b>Price:</b> Rs.{booking.trek.price} per person", normal_style))
    elements.append(Paragraph(f"<b>Pickup Location:</b> {booking.trek.pickup_location}", normal_style))
    elements.append(Paragraph(f"<b>Drop Location:</b> {booking.trek.drop_location}", normal_style))
    elements.append(Paragraph(f"<b>Meals Included:</b> {booking.trek.meals}", normal_style))
    elements.append(Paragraph(f"<b>Description:</b> {booking.trek.description}", normal_style))

    elements.append(Spacer(1, 30))

    # Footer Note
    footer_text = "Thank you for booking with us! We look forward to your adventure."
    elements.append(Paragraph(footer_text, normal_style))

    # Build the PDF
    doc.build(elements)

    return response


def chatbot_response(request):
    if request.method == "POST":
        user_input = request.POST.get("message", "").lower()

        # Check if user is asking about trekking
        if "trek" in user_input or "suggestions" in user_input:
            response_text = "Tell me your budget: Under ₹1K, ₹1K - ₹2K, ₹2K - ₹5K, Above ₹5K."
        else:
            response_text = "I'm here to help! Ask me about treks, weather, or travel plans."

        return JsonResponse({"text": response_text})

@staff_member_required
def admin_dashboard(request):
    total_bookings = Booking.objects.count()
    total_revenue = Booking.objects.aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0
    latest_bookings = Booking.objects.order_by('-date')[:6]
    total_users = CustomUser.objects.count()
    active_users = CustomUser.objects.filter(is_active=True).count()

    user_booking_data = Booking.objects.values('name').annotate(total_bookings=Count('id'))
    user_revenue_data = Booking.objects.values('name').annotate(total_revenue=Sum('total_price'))

    user_booking_labels = [entry['name'] for entry in user_booking_data]
    user_booking_values = [entry['total_bookings'] for entry in user_booking_data]
    
    user_revenue_labels = [entry['name'] for entry in user_revenue_data]
    user_revenue_values = [
        float(entry['total_revenue']) if entry['total_revenue'] else 0
        for entry in user_revenue_data
    ]

    top_trek_picks = Trek.objects.annotate(num_bookings=Count('booking')).order_by('-num_bookings')[:3]
    
    context = {
        'total_bookings': total_bookings,
        'total_revenue': float(total_revenue),
        'latest_bookings': latest_bookings,
        'total_users': total_users,
        'active_users': active_users,
        'user_booking_labels': json.dumps(user_booking_labels),
        'user_booking_values': json.dumps(user_booking_values),
        'user_revenue_labels': json.dumps(user_revenue_labels),
        'user_revenue_values': json.dumps(user_revenue_values),
        'top_trek_picks': top_trek_picks,
    }
    
    return render(request, 'admin/admin_dashboard.html', context)

