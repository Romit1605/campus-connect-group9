from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# ------------------------------------------------------------------
# Shared status choices reused across Ticket and LostFoundItem
# ------------------------------------------------------------------
STATUS_CHOICES = [
    ("Open",        "Open"),
    ("In Progress", "In Progress"),
    ("Resolved",    "Resolved"),
    ("Closed",      "Closed"),
    ("Claimed",     "Claimed"),
]


# ------------------------------------------------------------------
# 1. Category
# ------------------------------------------------------------------
class Category(models.Model):
    """Groups tickets and lost/found items into named categories."""

    CATEGORY_TYPE_CHOICES = [
        ("Ticket",    "Ticket"),
        ("LostFound", "LostFound"),
    ]

    name          = models.CharField(max_length=100)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE_CHOICES)
    description   = models.TextField(blank=True)
    is_active     = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering  = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name} ({self.category_type})"


# ------------------------------------------------------------------
# 2. UserProfile
# ------------------------------------------------------------------
class UserProfile(models.Model):
    """Extends Django's built-in User with extra campus details."""

    user          = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    student_id    = models.CharField(max_length=20, blank=True)
    phone         = models.CharField(max_length=20, blank=True)
    department    = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    bio           = models.TextField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


# Signal: automatically create a UserProfile whenever a new User is saved
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# ------------------------------------------------------------------
# 3. Ticket
# ------------------------------------------------------------------
class Ticket(models.Model):
    """A campus helpdesk support ticket raised by a student or staff."""

    PRIORITY_CHOICES = [
        ("Low",    "Low"),
        ("Medium", "Medium"),
        ("High",   "High"),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="tickets")
    title       = models.CharField(max_length=200)
    description = models.TextField()
    location    = models.CharField(max_length=200, blank=True)
    priority    = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="Medium")
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Open")
    attachment  = models.FileField(upload_to="ticket_attachments/", blank=True, null=True)
    is_public   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # Newest first

    def __str__(self):
        return f"[{self.status}] {self.title}"


# ------------------------------------------------------------------
# 4. LostFoundItem
# ------------------------------------------------------------------
class LostFoundItem(models.Model):
    """A lost or found item report submitted by a campus user."""

    ITEM_TYPE_CHOICES = [
        ("Lost Item",  "Lost Item"),
        ("Found Item", "Found Item"),
    ]

    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lost_found_items")
    item_type     = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    title         = models.CharField(max_length=200)
    description   = models.TextField()
    location      = models.CharField(max_length=200, blank=True)
    date_reported = models.DateField()
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Open")
    photo         = models.ImageField(upload_to="lost_found_photos/",     blank=True, null=True)
    document      = models.FileField(upload_to="lost_found_documents/",   blank=True, null=True)
    is_public     = models.BooleanField(default=True)
    contact_email = models.EmailField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # Newest first

    def __str__(self):
        return f"[{self.item_type}] {self.title}"


# ------------------------------------------------------------------
# 5. Comment
# ------------------------------------------------------------------
class Comment(models.Model):
    """A comment on either a Ticket or a LostFoundItem."""

    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    # A comment belongs to a ticket OR a lost/found item (not both)
    ticket         = models.ForeignKey(Ticket,        on_delete=models.CASCADE, blank=True, null=True, related_name="comments")
    lost_found_item= models.ForeignKey(LostFoundItem, on_delete=models.CASCADE, blank=True, null=True, related_name="comments")
    message        = models.TextField()
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]  # Oldest first (conversation order)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"


# ------------------------------------------------------------------
# 6. StatusUpdate
# ------------------------------------------------------------------
class StatusUpdate(models.Model):
    """Records every status change on a Ticket or LostFoundItem for audit trail."""

    updated_by     = models.ForeignKey(User, on_delete=models.CASCADE, related_name="status_updates")
    ticket         = models.ForeignKey(Ticket,        on_delete=models.CASCADE, blank=True, null=True, related_name="status_updates")
    lost_found_item= models.ForeignKey(LostFoundItem, on_delete=models.CASCADE, blank=True, null=True, related_name="status_updates")
    old_status     = models.CharField(max_length=20)
    new_status     = models.CharField(max_length=20)
    note           = models.TextField(blank=True)
    updated_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.old_status} → {self.new_status} by {self.updated_by.username}"


# ------------------------------------------------------------------
# 7. Announcement
# ------------------------------------------------------------------
class Announcement(models.Model):
    """A campus-wide announcement posted by staff or admin."""

    title      = models.CharField(max_length=200)
    message    = models.TextField()
    posted_by  = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="announcements")
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # Newest first

    def __str__(self):
        return self.title

