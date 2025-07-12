"""
URL Configuration for simple_django_framework project

What is this file? 🗺️
This is the MAIN URL configuration file for your entire Django project!
It's like the MAIN DIRECTORY at a building entrance that tells you:
1. Where to find each department (app)
2. Which elevator to take (URL routing)
3. Special routes like admin and static files

Think of this as the CENTRAL SWITCHBOARD for your website!
"""

# Import necessary Django components 📦
from django.contrib import admin  # Admin interface
from django.urls import path, include  # URL routing
from django.conf import settings  # Project settings
from django.conf.urls.static import static  # Static file serving
from django.views.generic import TemplateView  # Generic views
import logging  # For logging

# Get a logger for the main project 📝
logger = logging.getLogger('django')

# Main URL patterns for the entire project 🌐
urlpatterns = [
    
    # ADMIN INTERFACE 👑
    # URL: /admin/
    # This gives you access to Django's admin panel
    # Visit: http://127.0.0.1:8000/admin/
    path('admin/', admin.site.urls),
    
    # MAIN APP URLS 🏠
    # URL: / (all main app URLs start from root)
    # This includes ALL URLs from main_app/urls.py
    # Examples: /, /about/, /contact/, etc.
    path('', include('main_app.urls')),
    
    # AUTHENTICATION URLS (built-in Django auth) 🔐
    # URL: /accounts/
    # This gives you login, logout, password reset, etc.
    # Examples: /accounts/login/, /accounts/logout/
    path('accounts/', include('django.contrib.auth.urls')),
    
    # ROBOTS.TXT for search engines 🤖
    # URL: /robots.txt
    # This tells search engines which pages they can index
    path('robots.txt', 
         TemplateView.as_view(
             template_name='robots.txt', 
             content_type='text/plain'
         ),
         name='robots_txt'),
    
    # SITEMAP for search engines 🗺️
    # URL: /sitemap.xml
    # This helps search engines understand your site structure
    path('sitemap.xml', 
         TemplateView.as_view(
             template_name='sitemap.xml', 
             content_type='text/xml'
         ),
         name='sitemap'),
]

# DEVELOPMENT-ONLY URLs 🛠️
# These URLs are only available when DEBUG=True
if settings.DEBUG:
    
    # STATIC FILES SERVING 📁
    # In development, Django serves static files (CSS, JS, images)
    # In production, your web server (nginx, Apache) handles this
    urlpatterns += static(
        settings.STATIC_URL,  # URL prefix (/static/)
        document_root=settings.STATIC_ROOT  # File location
    )
    
    # MEDIA FILES SERVING 📸
    # Serves user-uploaded files (profile pictures, etc.)
    urlpatterns += static(
        settings.MEDIA_URL,  # URL prefix (/media/)
        document_root=settings.MEDIA_ROOT  # File location
    )
    
    # DEBUG TOOLBAR (if installed) 🔍
    # Uncomment these lines if you install django-debug-toolbar
    # try:
    #     import debug_toolbar
    #     urlpatterns += [
    #         path('__debug__/', include(debug_toolbar.urls)),
    #     ]
    # except ImportError:
    #     pass

# CUSTOM ERROR HANDLERS 🚨
# These handle HTTP errors with custom pages

# 404 Error - Page Not Found
handler404 = 'main_app.views.handle_404'

# 500 Error - Server Error  
handler500 = 'main_app.views.handle_500'

# You can also add handlers for other errors:
# handler403 = 'main_app.views.handle_403'  # Forbidden
# handler400 = 'main_app.views.handle_400'  # Bad Request

# FUTURE URL PATTERNS 🚀
# Uncomment these as you add more apps to your project:

# Blog app (if you create a separate blog app)
# urlpatterns += [
#     path('blog/', include('blog.urls')),
# ]

# API app (if you create a separate API app)
# urlpatterns += [
#     path('api/v1/', include('api.urls')),
# ]

# User profiles app (if you create a separate profiles app)
# urlpatterns += [
#     path('users/', include('profiles.urls')),
# ]

# E-commerce app (if you create a shop)
# urlpatterns += [
#     path('shop/', include('shop.urls')),
# ]

# Log URL configuration loading 📝
logger.info("Main project URL patterns loaded successfully")
logger.debug(f"Total main URL patterns: {len(urlpatterns)}")

# HELPFUL TIPS FOR PROJECT URLS 💡
"""
Project URL Tips:

1. KEEP IT ORGANIZED 📚
   - Put app-specific URLs in their own app/urls.py
   - Use include() to keep this file clean
   - Group related functionality together

2. USE MEANINGFUL PREFIXES 🏷️
   GOOD:
   - /blog/ for blog posts
   - /api/ for API endpoints  
   - /accounts/ for user management
   
   BAD:
   - /b/ (not descriptive)
   - /stuff/ (too vague)

3. PLAN FOR THE FUTURE 🔮
   - Reserve URL spaces for features you might add
   - Don't use generic names that might conflict
   - Think about SEO-friendly URLs

4. STATIC FILES IN PRODUCTION 🏭
   - Never serve static files through Django in production
   - Use nginx, Apache, or CDN instead
   - The static() calls here are ONLY for development

5. SECURITY CONSIDERATIONS 🛡️
   - Never expose admin URLs on obvious paths in production
   - Consider using custom admin URLs: /secret-admin/
   - Use HTTPS in production
   - Implement rate limiting for sensitive endpoints

6. URL VERSIONING FOR APIS 📱
   - Version your APIs: /api/v1/, /api/v2/
   - This allows backward compatibility
   - Easier to maintain multiple API versions

Example Production URL Structure:
/                    -> Homepage
/about/              -> About page
/contact/            -> Contact page
/blog/               -> Blog listing
/blog/my-post/       -> Individual blog post
/accounts/login/     -> Login page
/accounts/profile/   -> User profile
/api/v1/posts/       -> API endpoints
/admin/              -> Admin interface (consider custom path)
"""
