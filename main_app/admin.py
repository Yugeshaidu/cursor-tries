"""
Admin configuration for main_app

What is Django Admin? 👑
Django Admin is like a CONTROL ROOM for your website! It's a web interface where you can:
1. Add, edit, and delete data
2. Manage users and permissions
3. View statistics and reports
4. Perform administrative tasks

Think of it as the MANAGER'S OFFICE where you control everything!
"""

# Import necessary Django components 📦
from django.contrib import admin  # The admin framework
from django.utils.html import format_html  # For HTML formatting in admin
from django.urls import reverse  # For generating URLs
from django.utils import timezone  # For timezone handling
import logging  # For logging

# Import our models 🗄️
from .models import UserProfile, BlogPost, Comment, ContactMessage, Category

# Get a logger for this app 📝
logger = logging.getLogger('main_app')

# Custom admin configuration for UserProfile model 👤
@admin.register(UserProfile)  # Register this model with the admin
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for User Profiles 👤
    
    This class customizes how UserProfile appears in the Django admin.
    It's like designing the layout of a filing cabinet!
    """
    
    # Which fields to display in the list view 📋
    list_display = [
        'user',  # Show the username
        'bio_preview',  # Show first 50 characters of bio
        'website',  # Show website URL
        'created_at',  # Show when profile was created
        'profile_picture_preview',  # Show profile picture thumbnail
    ]
    
    # Which fields can be used for filtering 🔍
    list_filter = [
        'created_at',  # Filter by creation date
        'updated_at',  # Filter by update date
    ]
    
    # Which fields can be searched 🔎
    search_fields = [
        'user__username',  # Search by username (double underscore accesses related field)
        'user__email',  # Search by email
        'bio',  # Search in bio text
    ]
    
    # Read-only fields (can't be edited) 🔒
    readonly_fields = [
        'created_at',  # Creation time can't be changed
        'updated_at',  # Update time is automatic
        'profile_picture_preview',  # Show image preview
    ]
    
    # How to organize fields in the edit form 📝
    fieldsets = (
        # Basic Information section
        ('Basic Information', {
            'fields': ('user', 'bio')
        }),
        # Personal Details section
        ('Personal Details', {
            'fields': ('birth_date', 'website'),
            'classes': ('collapse',),  # This section can be collapsed
        }),
        # Profile Picture section
        ('Profile Picture', {
            'fields': ('profile_picture', 'profile_picture_preview'),
        }),
        # Timestamps section
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Collapsed by default
        }),
    )
    
    def bio_preview(self, obj):
        """
        Show first 50 characters of bio in list view ✂️
        
        Args:
            obj: The UserProfile object
            
        Returns:
            str: Truncated bio text
        """
        if obj.bio:
            return obj.bio[:50] + '...' if len(obj.bio) > 50 else obj.bio
        return 'No bio'
    bio_preview.short_description = 'Bio Preview'  # Column header name
    
    def profile_picture_preview(self, obj):
        """
        Show profile picture thumbnail in admin 🖼️
        
        Args:
            obj: The UserProfile object
            
        Returns:
            str: HTML for image thumbnail
        """
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                obj.profile_picture.url
            )
        return 'No picture'
    profile_picture_preview.short_description = 'Profile Picture'

# Custom admin configuration for BlogPost model 📝
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """
    Admin interface for Blog Posts 📝
    
    This provides a comprehensive interface for managing blog posts.
    """
    
    # List view configuration 📋
    list_display = [
        'title',  # Post title
        'author',  # Who wrote it
        'status',  # Draft/Published/Archived
        'view_count',  # How many views
        'is_featured',  # Featured post?
        'created_at',  # When created
        'published_at',  # When published
    ]
    
    # Add filters in the right sidebar 🔍
    list_filter = [
        'status',  # Filter by status
        'is_featured',  # Filter by featured posts
        'created_at',  # Filter by creation date
        'published_at',  # Filter by publication date
        'author',  # Filter by author
    ]
    
    # Search functionality 🔎
    search_fields = [
        'title',  # Search in title
        'content',  # Search in content
        'excerpt',  # Search in excerpt
        'author__username',  # Search by author username
    ]
    
    # Fields that auto-populate 🤖
    prepopulated_fields = {
        'slug': ('title',),  # Auto-generate slug from title
    }
    
    # Read-only fields 🔒
    readonly_fields = [
        'created_at',
        'updated_at',
        'view_count_display',
    ]
    
    # How many items per page 📄
    list_per_page = 25
    
    # Enable date hierarchy navigation 📅
    date_hierarchy = 'created_at'
    
    # Default ordering (newest first) 📊
    ordering = ['-created_at']
    
    # Organize edit form fields 📝
    fieldsets = (
        # Main Content
        ('Post Content', {
            'fields': ('title', 'slug', 'author', 'content', 'excerpt')
        }),
        # Publishing Options
        ('Publishing', {
            'fields': ('status', 'is_featured', 'published_at'),
        }),
        # Statistics
        ('Statistics', {
            'fields': ('view_count_display',),
            'classes': ('collapse',),
        }),
        # Timestamps
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    # Actions that can be performed on multiple posts 🔄
    actions = ['make_published', 'make_draft', 'make_featured']
    
    def view_count_display(self, obj):
        """
        Display view count with formatting 👁️
        
        Args:
            obj: The BlogPost object
            
        Returns:
            str: Formatted view count
        """
        return f"{obj.view_count:,} views"  # Add comma separators
    view_count_display.short_description = 'View Count'
    
    def make_published(self, request, queryset):
        """
        Action to publish selected posts ✅
        
        Args:
            request: The admin request
            queryset: Selected posts
        """
        updated = queryset.update(
            status='published',
            published_at=timezone.now()
        )
        # Log the action 📝
        logger.info(f"Admin {request.user.username} published {updated} blog posts")
        # Show success message
        self.message_user(request, f'{updated} posts were successfully published.')
    make_published.short_description = "Mark selected posts as published"
    
    def make_draft(self, request, queryset):
        """Action to make posts drafts 📝"""
        updated = queryset.update(status='draft')
        logger.info(f"Admin {request.user.username} made {updated} blog posts drafts")
        self.message_user(request, f'{updated} posts were moved to draft status.')
    make_draft.short_description = "Mark selected posts as draft"
    
    def make_featured(self, request, queryset):
        """Action to feature posts 🌟"""
        updated = queryset.update(is_featured=True)
        logger.info(f"Admin {request.user.username} featured {updated} blog posts")
        self.message_user(request, f'{updated} posts were marked as featured.')
    make_featured.short_description = "Mark selected posts as featured"
    
    def save_model(self, request, obj, form, change):
        """
        Custom save method for admin 💾
        
        This is called when saving a post through admin interface.
        
        Args:
            request: The admin request
            obj: The BlogPost object being saved
            form: The admin form
            change: True if updating, False if creating
        """
        # Log the admin action 📝
        if change:
            logger.info(f"Admin {request.user.username} updated blog post: {obj.title}")
        else:
            logger.info(f"Admin {request.user.username} created blog post: {obj.title}")
        
        # Call the parent save method
        super().save_model(request, obj, form, change)

# Inline admin for comments on blog posts 💬
class CommentInline(admin.TabularInline):
    """
    Inline admin for comments 💬
    
    This allows editing comments directly from the blog post edit page.
    It's like having sticky notes attached to a document!
    """
    model = Comment  # The model to edit inline
    extra = 0  # Don't show extra empty forms
    readonly_fields = ['created_at', 'updated_at']  # Read-only fields
    fields = ['author', 'content', 'is_approved', 'created_at']  # Fields to show

# Register the comment inline with BlogPost
# This is done by modifying the BlogPostAdmin class
BlogPostAdmin.inlines = (CommentInline,)

# Custom admin for Comment model 💬
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comments 💬"""
    
    list_display = [
        'post',  # Which post
        'author',  # Who commented
        'content_preview',  # First 50 chars of comment
        'is_approved',  # Approved?
        'created_at',  # When posted
    ]
    
    list_filter = [
        'is_approved',  # Filter by approval status
        'created_at',  # Filter by date
        'post__status',  # Filter by post status
    ]
    
    search_fields = [
        'content',  # Search in comment content
        'author__username',  # Search by author
        'post__title',  # Search by post title
    ]
    
    list_editable = ['is_approved']  # Allow quick editing of approval status
    
    actions = ['approve_comments', 'unapprove_comments']
    
    def content_preview(self, obj):
        """Show first 50 characters of comment 📝"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Comment Preview'
    
    def approve_comments(self, request, queryset):
        """Action to approve selected comments ✅"""
        updated = queryset.update(is_approved=True)
        logger.info(f"Admin {request.user.username} approved {updated} comments")
        self.message_user(request, f'{updated} comments were approved.')
    approve_comments.short_description = "Approve selected comments"
    
    def unapprove_comments(self, request, queryset):
        """Action to unapprove selected comments ❌"""
        updated = queryset.update(is_approved=False)
        logger.info(f"Admin {request.user.username} unapproved {updated} comments")
        self.message_user(request, f'{updated} comments were unapproved.')
    unapprove_comments.short_description = "Unapprove selected comments"

# Custom admin for ContactMessage model 📬
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for Contact Messages 📬"""
    
    list_display = [
        'name',  # Sender name
        'email',  # Sender email
        'subject',  # Message subject
        'status',  # Message status
        'created_at',  # When received
    ]
    
    list_filter = [
        'status',  # Filter by status
        'created_at',  # Filter by date
    ]
    
    search_fields = [
        'name',  # Search by name
        'email',  # Search by email
        'subject',  # Search by subject
        'message',  # Search in message content
    ]
    
    readonly_fields = ['created_at', 'resolved_at']
    
    list_editable = ['status']  # Allow quick status changes
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('name', 'email')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('Status Tracking', {
            'fields': ('status', 'created_at', 'resolved_at')
        }),
    )
    
    actions = ['mark_resolved', 'mark_spam']
    
    def mark_resolved(self, request, queryset):
        """Action to mark messages as resolved ✅"""
        updated = 0
        for message in queryset:
            message.mark_resolved()  # Use our custom method
            updated += 1
        logger.info(f"Admin {request.user.username} resolved {updated} contact messages")
        self.message_user(request, f'{updated} messages were marked as resolved.')
    mark_resolved.short_description = "Mark selected messages as resolved"
    
    def mark_spam(self, request, queryset):
        """Action to mark messages as spam 🚫"""
        updated = queryset.update(status='spam')
        logger.info(f"Admin {request.user.username} marked {updated} messages as spam")
        self.message_user(request, f'{updated} messages were marked as spam.')
    mark_spam.short_description = "Mark selected messages as spam"

# Custom admin for Category model 🏷️
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Categories 🏷️"""
    
    list_display = [
        'name',  # Category name
        'slug',  # URL slug
        'post_count',  # Number of posts
        'created_at',  # When created
    ]
    
    search_fields = ['name', 'description']
    
    prepopulated_fields = {'slug': ('name',)}  # Auto-generate slug
    
    readonly_fields = ['created_at', 'post_count']
    
    def post_count(self, obj):
        """Show number of published posts in category 📊"""
        count = obj.get_post_count()  # Use our custom method
        return f"{count} posts"
    post_count.short_description = 'Published Posts'

# Customize the admin site header and title 🎨
admin.site.site_header = 'Django Simple Framework Admin'  # Header text
admin.site.site_title = 'DSF Admin'  # Browser tab title
admin.site.index_title = 'Welcome to Django Simple Framework Administration'  # Homepage title

# Log when admin is accessed 📝
logger.info("Django admin configuration loaded successfully")
