from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .forms import EveLabFileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import EveLabFileForm, NetworkIssueForm, ConsultancyRequestForm, LabImageForm
from .models import EveLabFile, NetworkIssue, ConsultancyRequest, LabImage



def landing(request):
    return render(request, 'core/landing.html')

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

from django.contrib.auth.models import User

def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func


@admin_required
def upload_lab_image(request):
    if request.method == 'POST':
        form = LabImageForm(request.POST, request.FILES)
        if form.is_valid():
            lab_image = form.save(commit=False)
            lab_image.user = request.user
            lab_image.save()
            return redirect('home')
    else:
        form = LabImageForm()
    return render(request, 'core/upload_lab_image.html', {'form': form})

@admin_required
def upload_lab(request):
    if request.method == 'POST':
        form = EveLabFileForm(request.POST, request.FILES)
        if form.is_valid():
            lab = form.save(commit=False)
            lab.user = request.user
            lab.save()
            return redirect('labs_view')
    else:
        form = EveLabFileForm()
    return render(request, 'core/upload_lab.html', {'form': form})


def image_gallery(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

    # Fetch all images grouped by category
    image_categories = {}
    images = LabImage.objects.all()  # Fetch all images
    for image in images:
        category = image.category or "Uncategorized"
        image_categories.setdefault(category, []).append(image)
        # Check if it's an image and set the property
        image.is_image = image.file.url.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))

    return render(request, 'core/image_gallery.html', {
        'image_categories': image_categories,
    })


@login_required
def home(request):
    # Fetch labs uploaded by admins
    admins = User.objects.filter(is_superuser=True)
    labs = EveLabFile.objects.filter(user__in=admins).order_by('-uploaded_at')

    # Prepare image categories
    image_categories = {}
    categories = LabImage.objects.values_list('category', flat=True).distinct()

    for category in categories:
        image_categories[category] = LabImage.objects.filter(category=category).order_by('-uploaded_at')

    context = {
        'labs': labs,
        'image_categories': image_categories,
    }
    return render(request, 'core/home.html', context)



@login_required
def upload_lab(request):
    if not request.user.is_superuser:
        return render(request, 'core/no_permission.html', status=403)  # or redirect
    
    if request.method == 'POST':
        form = EveLabFileForm(request.POST, request.FILES)
        if form.is_valid():
            lab = form.save(commit=False)
            lab.user = request.user
            lab.save()
            return redirect('lab_list')
    else:
        form = EveLabFileForm()
    return render(request, 'core/upload_lab.html', {'form': form})

@login_required
def lab_list(request):
    # Get the admin user(s)
    admins = User.objects.filter(is_superuser=True)
    labs = EveLabFile.objects.filter(user__in=admins).order_by('-uploaded_at')
    return render(request, 'core/lab_list.html', {'labs': labs})


@login_required
def submit_issue(request):
    if request.method == 'POST':
        form = NetworkIssueForm(request.POST, user=request.user)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.save()
            return redirect('issue_success')
    else:
        form = NetworkIssueForm(user=request.user)
    return render(request, 'core/submit_issue.html', {'form': form})

@login_required
def issue_success(request):
    return render(request, 'core/issue_success.html')

@login_required
def consultancy_request(request):
    if request.method == 'POST':
        form = ConsultancyRequestForm(request.POST)
        if form.is_valid():
            consultancy = form.save(commit=False)
            consultancy.user = request.user
            consultancy.save()

            # Create Razorpay order for ₹7000 (7000*100 paise)
            amount = 7000 * 100
            order = razorpay_client.order.create({
                'amount': amount,
                'currency': 'INR',
                'payment_capture': '1'
            })
            consultancy.razorpay_order_id = order['id']
            consultancy.save()

            return render(request, 'core/consultancy_payment.html', {
                'consultancy': consultancy,
                'razorpay_key': settings.RAZORPAY_KEY_ID,
                'amount': amount,
                'order_id': order['id'],
            })
    else:
        form = ConsultancyRequestForm()
    return render(request, 'core/consultancy_request.html', {'form': form})

@csrf_exempt
@login_required
def razorpay_payment_verify(request):
    if request.method == 'POST':
        data = request.POST
        consultancy_id = data.get('consultancy_id')
        consultancy = get_object_or_404(ConsultancyRequest, id=consultancy_id)

        params_dict = {
            'razorpay_order_id': data.get('razorpay_order_id'),
            'razorpay_payment_id': data.get('razorpay_payment_id'),
            'razorpay_signature': data.get('razorpay_signature')
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
        except razorpay.errors.SignatureVerificationError:
            return HttpResponseBadRequest("Payment signature verification failed.")

        consultancy.razorpay_payment_id = params_dict['razorpay_payment_id']
        consultancy.razorpay_signature = params_dict['razorpay_signature']
        consultancy.paid = True
        consultancy.save()

        return JsonResponse({'status': 'Payment successful'})

    return HttpResponseBadRequest("Invalid method.")

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in user immediately after registration
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'core/register.html', {'form': form})

@login_required
def labs_view(request):
    admins = User.objects.filter(is_superuser=True)
    labs = EveLabFile.objects.filter(user__in=admins).order_by('-uploaded_at')

    # Group labs by type
    lab_categories = {
        'EVE Labs': labs.filter(lab_type='EVE'),
        'CML Labs': labs.filter(lab_type='CML'),
        'Packet Tracer Labs': labs.filter(lab_type='PT'),
    }

    return render(request, 'core/labs_view.html', {'lab_categories': lab_categories})

