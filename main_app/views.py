"""
Views for main_app

What are views? 👁️
Views are like WAITERS in a restaurant! They:
1. Take your order (HTTP request)
2. Go to the kitchen (process data, talk to models)
3. Bring you your food (HTTP response with HTML)

Think of views as the BRAIN of your web application - they decide what to show users!
"""

# Import necessary Django components 📦
from django.shortcuts import render, get_object_or_404  # Shortcuts for common tasks
from django.http import HttpResponse, JsonResponse      # Different types of responses
from django.views.generic import TemplateView          # Class-based views
from django.contrib.auth.decorators import login_required  # Require login for certain views
import logging  # For logging messages to our log files

# Get a logger for this app 📝
# This will write messages to our log files (remember settings.py?)
logger = logging.getLogger('main_app')

def home_view(request):
    """
    Home page view - this is what users see when they visit your website! 🏠
    
    Args:
        request: The HTTP request object (like a letter from the user)
                Contains info about the user, what they want, cookies, etc.
    
    Returns:
        HttpResponse: The web page to send back to the user
    """
    # Log that someone visited the home page 📝
    logger.info(f"Home page visited by user: {request.user}")
    
    # Create context data to pass to the template 📦
    # Context is like a box of information you give to the template
    context = {
        'page_title': 'Welcome to Django!',  # Title for the page
        'message': 'Hello from your Django app!',  # Welcome message
        'user': request.user,  # Current user (if logged in)
        'is_authenticated': request.user.is_authenticated,  # True if user is logged in
    }
    
    # Render the template with our context data 🎨
    # This combines the HTML template with our data
    return render(request, 'main_app/home.html', context)

def api_hello(request):
    """
    Simple API endpoint that returns JSON data 🌐
    
    This is an example of how to create API endpoints that return data
    instead of HTML pages. Great for mobile apps or JavaScript!
    
    Args:
        request: The HTTP request object
    
    Returns:
        JsonResponse: JSON data instead of HTML
    """
    # Log the API call 📝
    logger.info(f"API hello endpoint called by user: {request.user}")
    
    # Create data to return as JSON 📦
    data = {
        'message': 'Hello from Django API!',
        'status': 'success',
        'user': str(request.user),  # Convert user to string
        'timestamp': '2024-01-01',  # You'd use real timestamp here
    }
    
    # Return JSON response 📤
    # JsonResponse automatically converts Python dict to JSON
    return JsonResponse(data)

@login_required  # This decorator requires user to be logged in 🔐
def protected_view(request):
    """
    A view that requires login - only authenticated users can see this! 🔒
    
    The @login_required decorator automatically redirects non-logged-in users
    to the login page. It's like a bouncer at a club!
    
    Args:
        request: The HTTP request object
    
    Returns:
        HttpResponse: The protected page (only for logged-in users)
    """
    # Log that an authenticated user accessed protected content 📝
    logger.info(f"Protected view accessed by user: {request.user}")
    
    # Create context for the protected page 📦
    context = {
        'page_title': 'Protected Area',
        'message': f'Welcome {request.user.username}! This is a secret page.',
        'user': request.user,
    }
    
    # Render the protected template 🎨
    return render(request, 'main_app/protected.html', context)

def about_view(request):
    """
    About page view - tells users about your website 📖
    
    Args:
        request: The HTTP request object
    
    Returns:
        HttpResponse: The about page
    """
    # Log the about page visit 📝
    logger.info("About page visited")
    
    # Context for about page 📦
    context = {
        'page_title': 'About Us',
        'message': 'Learn more about our Django application!',
        'features': [  # List of features to display
            'User authentication',
            'Logging system',
            'Admin interface',
            'API endpoints',
            'Responsive design',
        ],
    }
    
    # Render about template 🎨
    return render(request, 'main_app/about.html', context)

class ContactView(TemplateView):
    """
    Class-based view for contact page 📞
    
    Class-based views are an alternative to function-based views.
    They're great when you need more complex behavior or want to reuse code.
    
    Think of class-based views as TEMPLATES for common website patterns!
    """
    
    # The template to use for this view 📄
    template_name = 'main_app/contact.html'
    
    def get_context_data(self, **kwargs):
        """
        Add extra context data to the template 📦
        
        This method is called automatically by Django to get data for the template.
        
        Returns:
            dict: Context data for the template
        """
        # Get the default context from parent class 📋
        context = super().get_context_data(**kwargs)
        
        # Add our custom data 📦
        context.update({
            'page_title': 'Contact Us',
            'contact_info': {
                'email': 'hello@yoursite.com',
                'phone': '+1-555-0123',
                'address': '123 Django Street, Python City',
            },
        })
        
        # Log that contact page was viewed 📝
        logger.info("Contact page viewed")
        
        # Return the complete context 📤
        return context

def error_test_view(request):
    """
    Test view to demonstrate error logging 🧪
    
    This view intentionally causes an error to show how our logging system works.
    In a real app, you'd remove this or protect it!
    
    Args:
        request: The HTTP request object
    
    Returns:
        HttpResponse: Never reached due to intentional error
    """
    # Log that someone is testing the error system 📝
    logger.warning("Error test view called - about to cause intentional error")
    
    try:
        # Intentionally cause an error 💥
        result = 1 / 0  # Division by zero error!
    except ZeroDivisionError as e:
        # Log the error with full details 📝
        logger.error(f"Intentional error in error_test_view: {e}")
        
        # Return a friendly error page instead of crashing 🛡️
        context = {
            'page_title': 'Error Test',
            'message': 'This was an intentional error to test logging!',
            'error_details': str(e),
        }
        return render(request, 'main_app/error_test.html', context)

def handle_404(request, exception):
    """
    Custom 404 error handler 🚫
    
    This function is called when a user tries to visit a page that doesn't exist.
    Instead of showing Django's default 404 page, we show our custom one!
    
    Args:
        request: The HTTP request object
        exception: The 404 exception that was raised
    
    Returns:
        HttpResponse: Custom 404 page
    """
    # Log the 404 error 📝
    logger.warning(f"404 error: {request.path} not found")
    
    # Context for 404 page 📦
    context = {
        'page_title': 'Page Not Found',
        'message': 'Sorry, the page you are looking for does not exist.',
        'requested_path': request.path,
    }
    
    # Render 404 template with 404 status code 🎨
    return render(request, 'main_app/404.html', context, status=404)

def handle_500(request):
    """
    Custom 500 error handler 💥
    
    This function is called when there's a server error (bug in your code).
    Instead of showing Django's default error page, we show our custom one!
    
    Args:
        request: The HTTP request object
    
    Returns:
        HttpResponse: Custom 500 page
    """
    # Log the server error 📝
    logger.error(f"500 server error occurred for path: {request.path}")
    
    # Context for 500 page 📦
    context = {
        'page_title': 'Server Error',
        'message': 'Something went wrong on our end. We are working to fix it!',
    }
    
    # Render 500 template with 500 status code 🎨
    return render(request, 'main_app/500.html', context, status=500)

# Example of a view that processes form data 📝
def contact_form_view(request):
    """
    Handle contact form submissions 📬
    
    This view shows how to handle both GET (show form) and POST (process form) requests.
    It's like having two functions in one!
    
    Args:
        request: The HTTP request object
    
    Returns:
        HttpResponse: Form page or success page
    """
    
    if request.method == 'POST':
        # User submitted the form - process the data 📤
        
        # Get form data from the request 📦
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        
        # Log the form submission 📝
        logger.info(f"Contact form submitted by {name} ({email})")
        
        # In a real app, you'd save this to database or send email 💾
        # For now, we just log it and show success message
        
        # Context for success page 📦
        context = {
            'page_title': 'Message Sent!',
            'message': f'Thank you {name}! We received your message.',
            'submitted_data': {
                'name': name,
                'email': email,
                'message': message,
            }
        }
        
        # Show success page 🎨
        return render(request, 'main_app/contact_success.html', context)
    
    else:
        # User wants to see the form - show it 📋
        
        # Log that form page was viewed 📝
        logger.info("Contact form page viewed")
        
        # Context for form page 📦
        context = {
            'page_title': 'Contact Form',
            'message': 'Send us a message!',
        }
        
        # Show form page 🎨
        return render(request, 'main_app/contact_form.html', context)
