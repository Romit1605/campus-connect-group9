from django.contrib import admin
from .models import (
    UserProfile, Category, Ticket,
    LostFoundItem, Comment, StatusUpdate, Announcement,
)


# ------------------------------------------------------------------
# UserProfile Admin
# ------------------------------------------------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display   = ("user", "student_id", "department", "phone", "created_at")
    list_filter    = ("department",)
    search_fields  = ("user__username", "student_id", "department")
    readonly_fields= ("created_at", "updated_at")


# ------------------------------------------------------------------
# Category Admin
# ------------------------------------------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display   = ("name", "category_type", "is_active", "created_at")
    list_filter    = ("category_type", "is_active")
    search_fields  = ("name",)
    readonly_fields= ("created_at",)


# ------------------------------------------------------------------
# Ticket Admin
# ------------------------------------------------------------------
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display   = ("title", "user", "category", "priority", "status", "is_public", "created_at")
    list_filter    = ("status", "priority", "category", "is_public")
    search_fields  = ("title", "description", "user__username")
    readonly_fields= ("created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        old_status = None
        if change:
            old_status = Ticket.objects.get(pk=obj.pk).status

        super().save_model(request, obj, form, change)

        if change and old_status is not None and old_status != obj.status:
            StatusUpdate.objects.create(
                updated_by=request.user,
                ticket=obj,
                old_status=old_status,
                new_status=obj.status,
                note="Status updated from admin panel",
            )


# ------------------------------------------------------------------
# LostFoundItem Admin
# ------------------------------------------------------------------
@admin.register(LostFoundItem)
class LostFoundItemAdmin(admin.ModelAdmin):
    list_display   = ("title", "user", "item_type", "status", "date_reported", "is_public", "created_at")
    list_filter    = ("item_type", "status", "is_public")
    search_fields  = ("title", "description", "user__username", "location")
    readonly_fields= ("created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        old_status = None
        if change:
            old_status = LostFoundItem.objects.get(pk=obj.pk).status

        super().save_model(request, obj, form, change)

        if change and old_status is not None and old_status != obj.status:
            StatusUpdate.objects.create(
                updated_by=request.user,
                lost_found_item=obj,
                old_status=old_status,
                new_status=obj.status,
                note="Status updated from admin panel",
            )


# ------------------------------------------------------------------
# Comment Admin
# ------------------------------------------------------------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display   = ("user", "ticket", "lost_found_item", "created_at")
    list_filter    = ("created_at",)
    search_fields  = ("user__username", "message")
    readonly_fields= ("created_at",)


# ------------------------------------------------------------------
# StatusUpdate Admin
# ------------------------------------------------------------------
@admin.register(StatusUpdate)
class StatusUpdateAdmin(admin.ModelAdmin):
    list_display   = ("updated_by", "ticket", "lost_found_item", "old_status", "new_status", "updated_at")
    list_filter    = ("new_status", "old_status")
    search_fields  = ("updated_by__username", "note")
    readonly_fields= ("updated_at",)


# ------------------------------------------------------------------
# Announcement Admin
# ------------------------------------------------------------------
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display   = ("title", "posted_by", "is_active", "created_at")
    list_filter    = ("is_active",)
    search_fields  = ("title", "message")
    readonly_fields= ("created_at", "updated_at")

