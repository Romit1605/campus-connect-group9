# from django.views.generic import TemplateView, View
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.urls import reverse
# from django.db.models import Q
# from django.http import JsonResponse
# from .forms import (
#     UserRegisterForm, UserUpdateForm, UserProfileUpdateForm,
#     TicketForm, LostFoundItemForm, CommentForm,
# )
# from .models import Ticket, LostFoundItem, Category, Comment, Announcement


# # ----------------------------------------------------------------
# # Phase 1 / Phase 7 — Home
# # ----------------------------------------------------------------
# class HomeView(View):
#     """
#     Public home page.
#     Phase 7: increments visit_count in session, records last_visited_page,
#     and sets a 'campus_portal_visited' cookie on first visit.
#     """

#     def get(self, request):
#         # --- Session tracking ---
#         request.session['visit_count'] = request.session.get('visit_count', 0) + 1
#         request.session['last_visited_page'] = 'Home'

#         total_tickets = Ticket.objects.count()
#         total_lost_found = LostFoundItem.objects.count()

#         open_tickets = Ticket.objects.filter(status__in=['Open', 'In Progress']).count()
#         open_items = LostFoundItem.objects.filter(status__in=['Open', 'In Progress']).count()

#         resolved_tickets = Ticket.objects.filter(status__in=['Resolved', 'Closed']).count()
#         resolved_items = LostFoundItem.objects.filter(status__in=['Resolved', 'Claimed']).count()

#         context = {
#             'total_reports': total_tickets + total_lost_found,
#             'open_reports': open_tickets + open_items,
#             'resolved_reports': resolved_tickets + resolved_items,
#             'lost_found_count': total_lost_found,
#             'ticket_count': total_tickets,
#         }

#         response = render(request, 'portal/home.html', context)

#         # --- Cookie: set once, valid for 1 year ---
#         if 'campus_portal_visited' not in request.COOKIES:
#             response.set_cookie('campus_portal_visited', 'yes', max_age=365 * 24 * 60 * 60)

#         return response


# def report_stats_api(request):
#     """Return live report statistics as JSON for a simple API endpoint."""
#     total_tickets = Ticket.objects.count()
#     total_lost_found_items = LostFoundItem.objects.count()

#     open_reports = Ticket.objects.filter(status__in=['Open', 'In Progress']).count() + LostFoundItem.objects.filter(status__in=['Open', 'In Progress']).count()
#     in_progress_reports = Ticket.objects.filter(status='In Progress').count() + LostFoundItem.objects.filter(status='In Progress').count()
#     resolved_reports = Ticket.objects.filter(status__in=['Resolved', 'Closed']).count() + LostFoundItem.objects.filter(status__in=['Resolved', 'Claimed']).count()
#     closed_reports = Ticket.objects.filter(status='Closed').count()
#     claimed_reports = LostFoundItem.objects.filter(status='Claimed').count()

#     data = {
#         'total_reports': total_tickets + total_lost_found_items,
#         'total_tickets': total_tickets,
#         'total_lost_found_items': total_lost_found_items,
#         'open_reports': open_reports,
#         'in_progress_reports': in_progress_reports,
#         'resolved_reports': resolved_reports,
#         'closed_reports': closed_reports,
#         'claimed_reports': claimed_reports,
#     }
#     return JsonResponse(data)


# # ----------------------------------------------------------------
# # Phase 3 — Registration
# # ----------------------------------------------------------------
# class RegisterView(View):
#     """Handles new user registration using UserRegisterForm."""

#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect('home')
#         return render(request, 'portal/register.html', {'form': UserRegisterForm()})

#     def post(self, request):
#         if request.user.is_authenticated:
#             return redirect('home')
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Account created for {form.cleaned_data["username"]}. You can now log in.')
#             return redirect('login')
#         return render(request, 'portal/register.html', {'form': form})


# # ----------------------------------------------------------------
# # Phase 3 — Profile
# # ----------------------------------------------------------------
# class ProfileView(LoginRequiredMixin, TemplateView):
#     """Displays the logged-in user's profile. Login required."""
#     template_name = 'portal/profile.html'


# class ProfileUpdateView(LoginRequiredMixin, View):
#     """Allows the logged-in user to update their own profile."""

#     def get(self, request):
#         return render(request, 'portal/profile_update.html', {
#             'user_form':    UserUpdateForm(instance=request.user),
#             'profile_form': UserProfileUpdateForm(instance=request.user.profile),
#         })

#     def post(self, request):
#         user_form    = UserUpdateForm(request.POST, instance=request.user)
#         profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Your profile has been updated successfully.')
#             return redirect('profile')
#         return render(request, 'portal/profile_update.html', {
#             'user_form':    user_form,
#             'profile_form': profile_form,
#         })


# # ----------------------------------------------------------------
# # Phase 4 — Ticket Submission
# # ----------------------------------------------------------------
# class TicketCreateView(LoginRequiredMixin, View):
#     """Allows a logged-in user to submit a new helpdesk ticket."""

#     def get(self, request):
#         return render(request, 'portal/ticket_form.html', {'form': TicketForm()})

#     def post(self, request):
#         form = TicketForm(request.POST, request.FILES)
#         if form.is_valid():
#             ticket = form.save(commit=False)
#             ticket.user = request.user
#             ticket.save()
#             messages.success(request, 'Your ticket has been submitted successfully.')
#             return redirect('report_list')
#         return render(request, 'portal/ticket_form.html', {'form': form})


# # ----------------------------------------------------------------
# # Phase 4 — Lost & Found Submission
# # ----------------------------------------------------------------
# class LostFoundCreateView(LoginRequiredMixin, View):
#     """Allows a logged-in user to submit a new lost or found item report."""

#     def get(self, request):
#         return render(request, 'portal/lostfound_form.html', {'form': LostFoundItemForm()})

#     def post(self, request):
#         form = LostFoundItemForm(request.POST, request.FILES)
#         if form.is_valid():
#             item = form.save(commit=False)
#             item.user = request.user
#             item.save()
#             messages.success(request, 'Your lost/found report has been submitted successfully.')
#             return redirect('report_list')
#         return render(request, 'portal/lostfound_form.html', {'form': form})


# # ----------------------------------------------------------------
# # Phase 5 / Phase 7 — Report List (search + filters + session keywords)
# # ----------------------------------------------------------------
# class ReportListView(View):
#     """
#     Public list of all reports (Tickets + LostFoundItems).
#     Supports keyword search and dropdown filters.
#     Only shows records where is_public=True.
#     Phase 7: saves search keyword in session (max 5, no duplicates).
#     """

#     def get(self, request):
#         q           = request.GET.get('q', '').strip()
#         report_type = request.GET.get('report_type', 'all')
#         status      = request.GET.get('status', '')
#         item_type   = request.GET.get('item_type', '')
#         category_id = request.GET.get('category', '')

#         # --- Phase 7: save keyword to session ---
#         if q:
#             keywords = request.session.get('recent_search_keywords', [])
#             if q in keywords:
#                 keywords.remove(q)       # remove old occurrence
#             keywords.insert(0, q)        # add to front
#             request.session['recent_search_keywords'] = keywords[:5]   # keep max 5

#         request.session['last_visited_page'] = 'Reports'

#         # --- Build Ticket queryset ---
#         tickets = []
#         if report_type in ('all', 'ticket'):
#             qs = Ticket.objects.filter(is_public=True).select_related('user', 'category')
#             if q:
#                 qs = qs.filter(
#                     Q(title__icontains=q) | Q(description__icontains=q) | Q(location__icontains=q)
#                 )
#             if status:
#                 qs = qs.filter(status=status)
#             if category_id:
#                 qs = qs.filter(category_id=category_id)
#             for t in qs:
#                 t.report_type = 'ticket'
#             tickets = list(qs)

#         # --- Build LostFoundItem queryset ---
#         lost_found = []
#         if report_type in ('all', 'lostfound'):
#             qs = LostFoundItem.objects.filter(is_public=True).select_related('user')
#             if q:
#                 qs = qs.filter(
#                     Q(title__icontains=q) | Q(description__icontains=q) | Q(location__icontains=q)
#                 )
#             if status:
#                 qs = qs.filter(status=status)
#             if item_type:
#                 qs = qs.filter(item_type=item_type)
#             for lf in qs:
#                 lf.report_type = 'lostfound'
#             lost_found = list(qs)

#         all_reports = sorted(tickets + lost_found, key=lambda r: r.created_at, reverse=True)
#         categories  = Category.objects.filter(category_type='Ticket', is_active=True)

#         return render(request, 'portal/report_list.html', {
#             'reports':     all_reports,
#             'total':       len(all_reports),
#             'q':           q,
#             'report_type': report_type,
#             'status':      status,
#             'item_type':   item_type,
#             'category_id': category_id,
#             'categories':  categories,
#         })


# # ----------------------------------------------------------------
# # Phase 5 / Phase 7 — Detail Pages
# # ----------------------------------------------------------------
# def _add_to_recently_viewed(request, entry):
#     """
#     Helper: insert an entry dict into the recently_viewed_reports session list.
#     Removes any prior entry with the same id+report_type, then prepends,
#     keeping at most 5 entries.
#     """
#     viewed = request.session.get('recently_viewed_reports', [])
#     viewed = [
#         v for v in viewed
#         if not (v['id'] == entry['id'] and v['report_type'] == entry['report_type'])
#     ]
#     viewed.insert(0, entry)
#     request.session['recently_viewed_reports'] = viewed[:5]


# class TicketDetailView(View):
#     """
#     Shows the full details of one public ticket.
#     Phase 7: records ticket in recently_viewed_reports session list.
#     Phase 8: allows logged-in users to add comments.
#     """

#     def get(self, request, pk):
#         ticket = get_object_or_404(Ticket, pk=pk, is_public=True)

#         # --- Phase 7: track recently viewed ---
#         _add_to_recently_viewed(request, {
#             'id':          ticket.pk,
#             'title':       ticket.title,
#             'status':      ticket.status,
#             'url':         reverse('ticket_detail', args=[ticket.pk]),
#             'report_type': 'Ticket',
#         })
#         request.session['last_visited_page'] = ticket.title

#         return render(request, 'portal/ticket_detail.html', {
#             'ticket': ticket,
#             'comments': ticket.comments.all(),
#             'comment_form': CommentForm(),
#             'status_updates': ticket.status_updates.all(),
#         })

#     def post(self, request, pk):
#         ticket = get_object_or_404(Ticket, pk=pk, is_public=True)

#         if not request.user.is_authenticated:
#             messages.error(request, 'Please log in to add a comment.')
#             return redirect('ticket_detail', pk=ticket.pk)

#         form = CommentForm(request.POST)
#         if form.is_valid():
#             Comment.objects.create(
#                 user=request.user,
#                 ticket=ticket,
#                 message=form.cleaned_data['message'].strip(),
#             )
#             messages.success(request, 'Your comment has been added successfully.')
#             return redirect('ticket_detail', pk=ticket.pk)

#         return render(request, 'portal/ticket_detail.html', {
#             'ticket': ticket,
#             'comments': ticket.comments.all(),
#             'comment_form': form,
#             'status_updates': ticket.status_updates.all(),
#         })


# class LostFoundDetailView(View):
#     """
#     Shows the full details of one public lost/found report.
#     Phase 7: records item in recently_viewed_reports session list.
#     Phase 8: allows logged-in users to add comments.
#     """

#     def get(self, request, pk):
#         item = get_object_or_404(LostFoundItem, pk=pk, is_public=True)

#         # --- Phase 7: track recently viewed ---
#         _add_to_recently_viewed(request, {
#             'id':          item.pk,
#             'title':       item.title,
#             'status':      item.status,
#             'url':         reverse('lostfound_detail', args=[item.pk]),
#             'report_type': 'Lost/Found',
#         })
#         request.session['last_visited_page'] = item.title

#         return render(request, 'portal/lostfound_detail.html', {
#             'item': item,
#             'comments': item.comments.all(),
#             'comment_form': CommentForm(),
#             'status_updates': item.status_updates.all(),
#         })

#     def post(self, request, pk):
#         item = get_object_or_404(LostFoundItem, pk=pk, is_public=True)

#         if not request.user.is_authenticated:
#             messages.error(request, 'Please log in to add a comment.')
#             return redirect('lostfound_detail', pk=item.pk)

#         form = CommentForm(request.POST)
#         if form.is_valid():
#             Comment.objects.create(
#                 user=request.user,
#                 lost_found_item=item,
#                 message=form.cleaned_data['message'].strip(),
#             )
#             messages.success(request, 'Your comment has been added successfully.')
#             return redirect('lostfound_detail', pk=item.pk)

#         return render(request, 'portal/lostfound_detail.html', {
#             'item': item,
#             'comments': item.comments.all(),
#             'comment_form': form,
#             'status_updates': item.status_updates.all(),
#         })


# # ----------------------------------------------------------------
# # Phase 6 — User Dashboard (My Reports)
# # ----------------------------------------------------------------
# class MyReportsView(LoginRequiredMixin, View):
#     """
#     Shows all tickets and lost/found items submitted by the logged-in user.
#     Acts as a personal dashboard / report history page.
#     """

#     def get(self, request):
#         tickets    = Ticket.objects.filter(user=request.user).order_by('-created_at')
#         lost_found = LostFoundItem.objects.filter(user=request.user).order_by('-created_at')
#         return render(request, 'portal/my_reports.html', {
#             'tickets':          tickets,
#             'lost_found':       lost_found,
#             'ticket_count':     tickets.count(),
#             'lost_found_count': lost_found.count(),
#         })


# class TicketUpdateView(LoginRequiredMixin, View):
#     """
#     Lets a logged-in user edit their own ticket.
#     Access is denied (redirect + error message) if the user is not the owner.
#     """

#     def _get_owned_ticket(self, request, pk):
#         ticket = get_object_or_404(Ticket, pk=pk)
#         if ticket.user != request.user:
#             messages.error(request, 'You do not have permission to edit that ticket.')
#             return None, redirect('my_reports')
#         return ticket, None

#     def get(self, request, pk):
#         ticket, err = self._get_owned_ticket(request, pk)
#         if err:
#             return err
#         return render(request, 'portal/ticket_update_form.html', {
#             'form': TicketForm(instance=ticket), 'ticket': ticket
#         })

#     def post(self, request, pk):
#         ticket, err = self._get_owned_ticket(request, pk)
#         if err:
#             return err
#         form = TicketForm(request.POST, request.FILES, instance=ticket)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your ticket has been updated successfully.')
#             return redirect('ticket_detail', pk=ticket.pk)
#         return render(request, 'portal/ticket_update_form.html', {'form': form, 'ticket': ticket})


# class LostFoundUpdateView(LoginRequiredMixin, View):
#     """
#     Lets a logged-in user edit their own lost/found report.
#     Access is denied (redirect + error message) if the user is not the owner.
#     """

#     def _get_owned_item(self, request, pk):
#         item = get_object_or_404(LostFoundItem, pk=pk)
#         if item.user != request.user:
#             messages.error(request, 'You do not have permission to edit that report.')
#             return None, redirect('my_reports')
#         return item, None

#     def get(self, request, pk):
#         item, err = self._get_owned_item(request, pk)
#         if err:
#             return err
#         return render(request, 'portal/lostfound_update_form.html', {
#             'form': LostFoundItemForm(instance=item), 'item': item
#         })

#     def post(self, request, pk):
#         item, err = self._get_owned_item(request, pk)
#         if err:
#             return err
#         form = LostFoundItemForm(request.POST, request.FILES, instance=item)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your report has been updated successfully.')
#             return redirect('lostfound_detail', pk=item.pk)
#         return render(request, 'portal/lostfound_update_form.html', {'form': form, 'item': item})


# # ----------------------------------------------------------------
# # Phase 7 — User History (sessions + cookie demo)
# # ----------------------------------------------------------------
# class UserHistoryView(LoginRequiredMixin, View):
#     """
#     Login-required page that displays session-tracked data:
#     visit count, recently viewed reports, recent search keywords,
#     last visited page, and whether the campus_portal_visited cookie is set.
#     """

#     def get(self, request):
#         return render(request, 'portal/user_history.html', {
#             'visit_count':      request.session.get('visit_count', 0),
#             'recently_viewed':  request.session.get('recently_viewed_reports', []),
#             'recent_keywords':  request.session.get('recent_search_keywords', []),
#             'last_visited':     request.session.get('last_visited_page', '—'),
#             'has_cookie':       'campus_portal_visited' in request.COOKIES,
#         })


# # ----------------------------------------------------------------
# # Phase 10 / Phase 11 — Announcements and static pages
# # ----------------------------------------------------------------
# class AnnouncementListView(View):
#     """Public page showing active announcements and recent resolved updates."""

#     def get(self, request):
#         announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')

#         resolved_tickets = Ticket.objects.filter(
#             is_public=True,
#             status__in=['Resolved', 'Closed'],
#         ).order_by('-updated_at', '-created_at')[:5]

#         resolved_items = LostFoundItem.objects.filter(
#             is_public=True,
#             status__in=['Resolved', 'Claimed'],
#         ).order_by('-updated_at', '-created_at')[:5]

#         return render(request, 'portal/announcements.html', {
#             'announcements': announcements,
#             'resolved_tickets': resolved_tickets,
#             'resolved_items': resolved_items,
#         })


# class AboutView(TemplateView):
#     """Public About page describing the campus portal."""
#     template_name = 'portal/about.html'


# class ContactView(TemplateView):
#     """Public Contact page with simple support information."""
#     template_name = 'portal/contact.html'
