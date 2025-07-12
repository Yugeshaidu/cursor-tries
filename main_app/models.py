"""
Models for main_app

What are models? 🗄️
Models are like BLUEPRINTS for your database! They:
1. Define what kind of data you want to store (like a form template)
2. Create database tables automatically
3. Provide methods to save, retrieve, and manipulate data

Think of models as the FILING CABINET organizer for your website's data!
"""

# Import necessary Django components 📦
from django.db import models  # The base model class
from django.contrib.auth.models import User  # Built-in user model
from django.urls import reverse  # For generating URLs
from django.utils import timezone  # For timezone-aware dates
import logging  # For logging

# Get a logger for this app 📝
logger = logging.getLogger('main_app')

class UserProfile(models.Model):
    """
    Extended user profile model 👤
    
    Django comes with a basic User model (username, password, email).
    This model extends it with additional information!
    
    This is like adding extra pages to a person's file folder.
    """
    
    # Link to the built-in User model (one-to-one relationship) 🔗
    # This means each User gets exactly one UserProfile
    user = models.OneToOneField(
        User,  # The model we're linking to
        on_delete=models.CASCADE,  # If user is deleted, delete this profile too
        help_text="The user this profile belongs to"
    )
    
    # Additional profile fields 📋
    bio = models.TextField(
        max_length=500,  # Maximum 500 characters
        blank=True,  # This field can be left empty
        help_text="Tell us about yourself!"
    )
    
    birth_date = models.DateField(
        null=True,  # Database can store NULL
        blank=True,  # Form can be left empty
        help_text="Your birth date (optional)"
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pics/',  # Where to store uploaded images
        null=True,  # Can be empty in database
        blank=True,  # Can be empty in forms
        help_text="Upload a profile picture"
    )
    
    website = models.URLField(
        blank=True,  # Optional field
        help_text="Your personal website (optional)"
    )
    
    # Timestamps - when was this created/updated? 📅
    created_at = models.DateTimeField(
        auto_now_add=True,  # Automatically set when profile is created
        help_text="When this profile was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,  # Automatically updated every time profile is saved
        help_text="When this profile was last updated"
    )
    
    class Meta:
        """
        Metadata for the model 📋
        
        Meta class contains information ABOUT the model, not data fields.
        It's like the label on the outside of a file folder.
        """
        verbose_name = "User Profile"  # Human-readable name (singular)
        verbose_name_plural = "User Profiles"  # Human-readable name (plural)
        ordering = ['-created_at']  # Default ordering (newest first)
    
    def __str__(self):
        """
        String representation of the model 📝
        
        This is what shows up when you print() a UserProfile object.
        It's like the title on a file folder.
        
        Returns:
            str: Human-readable representation
        """
        return f"{self.user.username}'s Profile"
    
    def get_absolute_url(self):
        """
        Get the URL for this profile 🔗
        
        This method returns the URL where users can view this profile.
        
        Returns:
            str: URL path to view this profile
        """
        return reverse('profile_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        """
        Custom save method 💾
        
        This method is called every time the profile is saved.
        We can add custom logic here!
        
        Args:
            *args: Variable arguments
            **kwargs: Keyword arguments
        """
        # Log when a profile is saved 📝
        if self.pk:  # If profile already exists (updating)
            logger.info(f"Updating profile for user: {self.user.username}")
        else:  # If this is a new profile (creating)
            logger.info(f"Creating new profile for user: {self.user.username}")
        
        # Call the parent save method to actually save to database 💾
        super().save(*args, **kwargs)

class BlogPost(models.Model):
    """
    Blog post model 📝
    
    This model represents a blog post on your website.
    Each blog post has a title, content, author, and timestamps.
    """
    
    # The post title 🎯
    title = models.CharField(
        max_length=200,  # Maximum 200 characters
        help_text="The title of your blog post"
    )
    
    # URL-friendly version of the title 🔗
    # This is used in URLs like /blog/my-awesome-post/
    slug = models.SlugField(
        max_length=200,  # Maximum 200 characters
        unique=True,  # No two posts can have the same slug
        help_text="URL-friendly version of title (auto-generated)"
    )
    
    # The author of the post 👤
    author = models.ForeignKey(
        User,  # Link to User model
        on_delete=models.CASCADE,  # If user is deleted, delete their posts
        related_name='blog_posts',  # Access user's posts with user.blog_posts
        help_text="Who wrote this post"
    )
    
    # The main content 📄
    content = models.TextField(
        help_text="The main content of your blog post"
    )
    
    # Short summary for previews 📋
    excerpt = models.TextField(
        max_length=300,  # Maximum 300 characters
        blank=True,  # Optional field
        help_text="Short summary of the post (optional)"
    )
    
    # Post status choices 📊
    STATUS_CHOICES = [
        ('draft', 'Draft'),      # Post is being written
        ('published', 'Published'),  # Post is live on website
        ('archived', 'Archived'),    # Post is hidden from public
    ]
    
    status = models.CharField(
        max_length=10,  # Maximum 10 characters
        choices=STATUS_CHOICES,  # Must be one of the choices above
        default='draft',  # New posts start as drafts
        help_text="The current status of this post"
    )
    
    # View count for analytics 📊
    view_count = models.PositiveIntegerField(
        default=0,  # Start with 0 views
        help_text="How many times this post has been viewed"
    )
    
    # Featured post? 🌟
    is_featured = models.BooleanField(
        default=False,  # Not featured by default
        help_text="Should this post be featured on the homepage?"
    )
    
    # Timestamps 📅
    created_at = models.DateTimeField(
        auto_now_add=True,  # Set when post is created
        help_text="When this post was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,  # Updated every time post is saved
        help_text="When this post was last updated"
    )
    
    published_at = models.DateTimeField(
        null=True,  # Can be empty
        blank=True,  # Can be empty in forms
        help_text="When this post was published"
    )
    
    class Meta:
        """Metadata for BlogPost model"""
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-created_at']  # Newest posts first
        indexes = [
            models.Index(fields=['status', 'created_at']),  # Database index for faster queries
            models.Index(fields=['author', 'status']),      # Another useful index
        ]
    
    def __str__(self):
        """String representation"""
        return f"{self.title} by {self.author.username}"
    
    def get_absolute_url(self):
        """Get URL for this post"""
        return reverse('blog_post_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        """Custom save method"""
        # If post is being published for the first time
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()  # Set publication time
            logger.info(f"Publishing blog post: {self.title}")
        
        # Log the save action
        if self.pk:
            logger.info(f"Updating blog post: {self.title}")
        else:
            logger.info(f"Creating new blog post: {self.title}")
        
        # Call parent save method
        super().save(*args, **kwargs)
    
    def increment_view_count(self):
        """
        Increment the view count for this post 👁️
        
        Call this method when someone views the post.
        """
        self.view_count += 1  # Add 1 to view count
        self.save(update_fields=['view_count'])  # Only update view_count field
        logger.debug(f"View count incremented for post: {self.title}")

class Comment(models.Model):
    """
    Comment model 💬
    
    This model represents comments on blog posts.
    Users can leave comments on any published blog post.
    """
    
    # The blog post this comment belongs to 📝
    post = models.ForeignKey(
        BlogPost,  # Link to BlogPost model
        on_delete=models.CASCADE,  # Delete comments if post is deleted
        related_name='comments',  # Access post comments with post.comments
        help_text="The blog post this comment is on"
    )
    
    # Who wrote the comment 👤
    author = models.ForeignKey(
        User,  # Link to User model
        on_delete=models.CASCADE,  # Delete comments if user is deleted
        help_text="Who wrote this comment"
    )
    
    # The comment content 💬
    content = models.TextField(
        max_length=1000,  # Maximum 1000 characters
        help_text="Your comment content"
    )
    
    # Comment approval status 👍
    is_approved = models.BooleanField(
        default=True,  # Automatically approve comments (you might want False)
        help_text="Is this comment approved for display?"
    )
    
    # Timestamps 📅
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this comment was posted"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this comment was last edited"
    )
    
    class Meta:
        """Metadata for Comment model"""
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['created_at']  # Oldest comments first (chronological order)
        indexes = [
            models.Index(fields=['post', 'created_at']),  # For fast comment loading
        ]
    
    def __str__(self):
        """String representation"""
        return f"Comment by {self.author.username} on {self.post.title}"
    
    def save(self, *args, **kwargs):
        """Custom save method"""
        # Log comment creation/update
        if self.pk:
            logger.info(f"Updating comment by {self.author.username}")
        else:
            logger.info(f"New comment by {self.author.username} on post: {self.post.title}")
        
        # Call parent save method
        super().save(*args, **kwargs)

class ContactMessage(models.Model):
    """
    Contact message model 📬
    
    This model stores messages sent through the contact form.
    It's like a digital mailbox for your website!
    """
    
    # Sender information 👤
    name = models.CharField(
        max_length=100,
        help_text="Full name of the person contacting us"
    )
    
    email = models.EmailField(
        help_text="Email address for replies"
    )
    
    subject = models.CharField(
        max_length=200,
        help_text="Subject of the message"
    )
    
    # The message content 💬
    message = models.TextField(
        help_text="The actual message content"
    )
    
    # Status tracking 📊
    STATUS_CHOICES = [
        ('new', 'New'),            # Just received
        ('in_progress', 'In Progress'),  # Being handled
        ('resolved', 'Resolved'),      # Completed
        ('spam', 'Spam'),             # Marked as spam
    ]
    
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='new',
        help_text="Current status of this message"
    )
    
    # Timestamps 📅
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this message was received"
    )
    
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this message was resolved"
    )
    
    class Meta:
        """Metadata for ContactMessage model"""
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']  # Newest messages first
    
    def __str__(self):
        """String representation"""
        return f"Message from {self.name}: {self.subject}"
    
    def mark_resolved(self):
        """
        Mark this message as resolved ✅
        
        Call this method when you've handled the message.
        """
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        self.save()
        logger.info(f"Marked contact message as resolved: {self.subject}")

# Example of a more advanced model with custom methods
class Category(models.Model):
    """
    Category model for organizing blog posts 🏷️
    
    This model represents categories that blog posts can belong to.
    Examples: Technology, Travel, Food, etc.
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,  # No duplicate category names
        help_text="Category name"
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="URL-friendly version of category name"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Description of this category"
    )
    
    # Many-to-many relationship with blog posts
    # This means a post can have multiple categories, and a category can have multiple posts
    posts = models.ManyToManyField(
        BlogPost,
        blank=True,
        related_name='categories',
        help_text="Blog posts in this category"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']  # Alphabetical order
    
    def __str__(self):
        return self.name
    
    def get_post_count(self):
        """
        Get the number of published posts in this category 📊
        
        Returns:
            int: Number of published posts
        """
        return self.posts.filter(status='published').count()
    
    def get_absolute_url(self):
        """Get URL for this category"""
        return reverse('category_detail', kwargs={'slug': self.slug})
