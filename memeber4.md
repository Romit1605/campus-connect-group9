# Member 4 — Search, Filters & User Dashboard

> **Viva tip:** Be ready to explain every line in the files below.
> The examiner may ask you to live-edit your views on PyCharm.

---

## 🗂️ Files You Own — Upload Your Code Here

### Python files
| File path (from project root) | What you write |
|---|---|
| `portal/models.py` | `StatusUpdate` model |
| `portal/views.py` | `ReportListView`, `MyReportsView`, `TicketUpdateView` (ownership check logic), `LostFoundUpdateView` (ownership check logic) |
| `portal/urls.py` | URL patterns: `reports/`, `my-reports/` |
| `portal/admin.py` | Register `StatusUpdate` in Django admin |

### Template files
| Template path | Purpose |
|---|---|
| `templates/portal/report_list.html` | Search bar + 4 dropdown filters + report cards grid |
| `templates/portal/my_reports.html` | Personal dashboard showing user's own tickets + lost/found reports |

---

## ✅ Requirements You Cover

| Project requirement | How you cover it |
|---|---|
| Creating & editing models | `StatusUpdate` model (audit trail) |
| Class-based views | `ReportListView`, `MyReportsView` |
| Search bar | Keyword search input (`q` GET param) searching title, description, location |
| Dropdown filters | 4 dropdowns: Report Type, Status, Item Type, Category |
| `Q` objects for search | `Q(title__icontains=q) \| Q(description__icontains=q) \| Q(location__icontains=q)` |
| Registered vs guest UI | `MyReportsView` uses `LoginRequiredMixin`; public list visible to all |
| Bootstrap styling | Cards, badges, filter form in `report_list.html` |

---

## 🧩 Key Classes to Implement

```python
# portal/models.py
class StatusUpdate(models.Model):
    updated_by      = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket          = models.ForeignKey('Ticket', on_delete=models.CASCADE, blank=True, null=True)
    lost_found_item = models.ForeignKey('LostFoundItem', on_delete=models.CASCADE, blank=True, null=True)
    old_status      = models.CharField(max_length=20)
    new_status      = models.CharField(max_length=20)
    note            = models.TextField(blank=True)
    updated_at      = models.DateTimeField(auto_now_add=True)

# portal/views.py
class ReportListView(View):
    """
    GET params: q (keyword), report_type, status, item_type, category
    Uses Q objects to filter Ticket and LostFoundItem querysets.
    Also saves search keyword to session (recent_search_keywords).
    """
    def get(self, request): ...

class MyReportsView(LoginRequiredMixin, View):
    """Shows all tickets and lost/found items for the logged-in user."""
    def get(self, request): ...
```

### Search logic skeleton
```python
from django.db.models import Q

q = request.GET.get('q', '').strip()
qs = Ticket.objects.filter(is_public=True)
if q:
    qs = qs.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(location__icontains=q)
    )
```

---

## 📌 Git Commit Convention
```
Member4: <short description>
# e.g.
Member4: Add StatusUpdate model
Member4: Implement ReportListView with keyword search and dropdown filters
Member4: Implement MyReportsView dashboard
Member4: Add report_list.html with search bar and filter dropdowns
Member4: Add my_reports.html personal dashboard template
```
