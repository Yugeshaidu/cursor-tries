"""
URL Configuration for main_app

What are URLs? 🗺️
URLs are like a MAP for your website! They tell Django:
1. Which view function to call for each web address
2. How to extract parameters from URLs (like IDs)
3. What names to give URLs so you can reference them

Think of URLs as a RECEPTIONIST who directs visitors to the right office!
"""

# Import necessary Django components 📦
from django.urls import path, include  # For URL routing
from django.views.generic import TemplateView  # Generic views
import logging  # For logging

# Import our views 👁️
from . import views

# Get a logger for this app 📝
logger = logging.getLogger('main_app')

# Define the app name for URL namespacing 📋
# This allows us to use 'main_app:home' instead of just 'home'
# Prevents conflicts if multiple apps have same URL names
app_name = 'main_app'

# URL patterns - the heart of URL routing! 💖
# Each path() connects a URL pattern to a view function
urlpatterns = [
    
    # HOME PAGE 🏠
    # URL: / (root of website)
    # View: home_view function
    # Name: 'home' (used in templates like {% url 'main_app:home' %})
    path('', views.home_view, name='home'),
    
    # ABOUT PAGE 📖
    # URL: /about/
    # View: about_view function
    # Name: 'about'
    path('about/', views.about_view, name='about'),
    
    # CONTACT PAGES 📞
    # URL: /contact/
    # View: ContactView class-based view
    # Name: 'contact'
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # Contact form handling
    # URL: /contact/form/
    # View: contact_form_view function (handles GET and POST)
    # Name: 'contact_form'
    path('contact/form/', views.contact_form_view, name='contact_form'),
    
    # PROTECTED AREA 🔒
    # URL: /protected/
    # View: protected_view (requires login)
    # Name: 'protected'
    path('protected/', views.protected_view, name='protected'),
    
    # API ENDPOINTS 🌐
    # URL: /api/hello/
    # View: api_hello function (returns JSON)
    # Name: 'api_hello'
    path('api/hello/', views.api_hello, name='api_hello'),
    
    # TESTING AND DEBUGGING 🧪
    # URL: /test-error/
    # View: error_test_view (intentionally causes error)
    # Name: 'error_test'
    # Note: Remove this in production!
    path('test-error/', views.error_test_view, name='error_test'),
    
    # STATIC PAGES using TemplateView 📄
    # These are simple pages that don't need custom view logic
    
    # Privacy Policy page
    # URL: /privacy/
    # View: Django's built-in TemplateView
    # Template: main_app/privacy.html
    path('privacy/', 
         TemplateView.as_view(template_name='main_app/privacy.html'),
         name='privacy'),
    
    # Terms of Service page
    # URL: /terms/
    path('terms/', 
         TemplateView.as_view(template_name='main_app/terms.html'),
         name='terms'),
    
    # Help page
    # URL: /help/
    path('help/', 
         TemplateView.as_view(
             template_name='main_app/help.html',
             extra_context={'page_title': 'Help & Support'}  # Pass extra data
         ),
         name='help'),
]

# FUTURE URL PATTERNS 🚀
# Uncomment these as you develop more features:

# Blog URLs (for future blog functionality)
blog_patterns = [
    # Blog home page
    # path('blog/', views.blog_list, name='blog_list'),
    
    # Individual blog post
    # path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # Blog by category
    # path('blog/category/<slug:category>/', views.blog_by_category, name='blog_category'),
    
    # Create new blog post (for logged-in users)
    # path('blog/create/', views.blog_create, name='blog_create'),
]

# User profile URLs (for future user functionality)
profile_patterns = [
    # User profile page
    # path('profile/<int:user_id>/', views.profile_detail, name='profile_detail'),
    
    # Edit profile
    # path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # User's blog posts
    # path('profile/<int:user_id>/posts/', views.user_posts, name='user_posts'),
]

# API URLs (for future API development)
api_patterns = [
    # List all blog posts as JSON
    # path('api/posts/', views.api_post_list, name='api_post_list'),
    
    # Get specific post as JSON
    # path('api/posts/<int:post_id>/', views.api_post_detail, name='api_post_detail'),
    
    # Create comment via API
    # path('api/posts/<int:post_id>/comments/', views.api_create_comment, name='api_create_comment'),
]

# Add future patterns to main urlpatterns when ready:
# urlpatterns += blog_patterns
# urlpatterns += profile_patterns  
# urlpatterns += api_patterns

# URL PATTERNS WITH PARAMETERS 🎯
# These examples show how to capture parts of URLs as parameters

parameter_examples = [
    # Capture integer parameter
    # URL: /post/123/ captures 123 as post_id
    # path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    
    # Capture string parameter (slug)
    # URL: /article/my-awesome-post/ captures 'my-awesome-post' as slug
    # path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    
    # Capture string parameter
    # URL: /user/john/ captures 'john' as username
    # path('user/<str:username>/', views.user_profile, name='user_profile'),
    
    # Multiple parameters
    # URL: /blog/2024/01/my-post/ captures year, month, and slug
    # path('blog/<int:year>/<int:month>/<slug:slug>/', 
    #      views.blog_post_by_date, name='blog_post_by_date'),
]

# REGULAR EXPRESSION PATTERNS 🎭
# For more complex URL patterns, you can use regular expressions

from django.urls import re_path  # Import for regex patterns

regex_examples = [
    # Match phone numbers: /phone/555-123-4567/
    # re_path(r'^phone/(?P<phone>\d{3}-\d{3}-\d{4})/$', 
    #         views.phone_lookup, name='phone_lookup'),
    
    # Match dates: /archive/2024/01/15/
    # re_path(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',
    #         views.archive_detail, name='archive_detail'),
]

# ERROR HANDLING URLs 🚨
# These handle special error cases

error_patterns = [
    # Custom 404 page (when page not found)
    # This is usually handled in the main project urls.py
    # path('404/', views.custom_404, name='404'),
    
    # Custom 500 page (when server error occurs)
    # path('500/', views.custom_500, name='500'),
]

# CONDITIONAL URL PATTERNS 🔀
# You can add URLs conditionally based on settings

from django.conf import settings

# Only add debug URLs in development
if settings.DEBUG:
    debug_patterns = [
        # URL: /debug/info/
        path('debug/info/', 
             TemplateView.as_view(template_name='main_app/debug_info.html'),
             name='debug_info'),
    ]
    urlpatterns += debug_patterns

# Log URL configuration loading 📝
logger.info(f"URL patterns loaded for {app_name} app")
logger.debug(f"Total URL patterns: {len(urlpatterns)}")

# HELPFUL TIPS FOR URL PATTERNS 💡
"""
URL Pattern Tips:

1. ORDER MATTERS! 📊
   URLs are matched top to bottom. Put specific patterns before general ones.
   
   GOOD:
   path('blog/create/', views.blog_create),  # Specific
   path('blog/<slug:slug>/', views.blog_detail),  # General
   
   BAD:
   path('blog/<slug:slug>/', views.blog_detail),  # This catches everything!
   path('blog/create/', views.blog_create),  # This will never be reached

2. ALWAYS NAME YOUR URLS 🏷️
   Use descriptive names so you can reference them in templates and views.
   
   GOOD: name='blog_detail'
   BAD: No name

3. USE PARAMETERS WISELY 🎯
   <int:id> - for integers (database IDs)
   <str:username> - for strings (usernames)
   <slug:slug> - for URL-friendly strings (blog post slugs)
   
4. KEEP URLS SIMPLE AND CLEAN 🧹
   /blog/my-awesome-post/ ✅
   /blog.php?id=123&action=view ❌

5. USE TRAILING SLASHES CONSISTENTLY 📏
   Django prefers URLs with trailing slashes: /about/
   But be consistent throughout your app.

6. GROUP RELATED URLS 📚
   Use include() to organize URLs into separate files:
   path('blog/', include('blog.urls'))
"""