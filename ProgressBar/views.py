from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_GET

from .models import Progress, Update, ProgressHistory
from .forms import ProgressForm, UpdateForm, ProgressCreateForm


def create_progress_bar(request):
    """Tworzy nowy pasek postępu i zwraca unikalne linki."""
    progress = Progress.objects.create()
    return render(request, 'created.html', {
        'public_link': f"/view/{progress.public_id}/",
        'admin_link': f"/admin/{progress.admin_id}/"
    })
def progress_view(request, public_id):
    """Widok podglądu progress bara na podstawie public_id"""
    try:
        progress = Progress.objects.get(public_id=public_id)
        progress.increment_view_count()
        updates = progress.updates.all()  # Pobranie wszystkich aktualizacji powiązanych z postępem
    except Progress.DoesNotExist:
        raise Http404("Progress bar not found")

    return render(request, 'progress.html', {'progress': progress, 'updates': updates})



def admin_panel(request, admin_id):
    progress = get_object_or_404(Progress, admin_id=admin_id)

    history = ProgressHistory.objects.filter(progress=progress).order_by('created_at')
    history_data = [{"x": record.created_at, "y": record.percentage} for record in history]

    if request.method == 'POST':
        if 'progress_form' in request.POST:
            # Obsługuje formularz do ustawienia procentu paska
            progress_form = ProgressForm(request.POST, instance=progress)
            if progress_form.is_valid():

                progress_form.save()

                # Zapisz historię zmiany procentu
                ProgressHistory.objects.create(progress=progress, percentage=progress.percentage)

        elif 'update_form' in request.POST:
            # Obsługuje formularz do dodawania nowej aktualizacji
            update_form = UpdateForm(request.POST)
            if update_form.is_valid():
                update = update_form.save(commit=False)
                update.progress = progress
                update.save()

        return redirect(f'/admin-panel/{progress.admin_id}/')

    else:
        progress_form = ProgressForm(instance=progress)
        update_form = UpdateForm()

    updates = progress.updates.all()

    return render(request, 'admin_panel.html', {
        'progress_form': progress_form,
        'update_form': update_form,
        'updates': updates,
        'admin_id': admin_id,
        'view_count': progress.view_count,  # Liczba wejść na publiczny link
        'history_data': history_data,  # Dane do wykresu
        'progress': progress,  # Przekazujemy obiekt progress, aby mieć dostęp do public_id
    })

def create_progress_view(request):
    """Widok tworzenia nowego progress bara"""
    if request.method == 'POST':
        form = ProgressCreateForm(request.POST)
        if form.is_valid():
            progress = form.save()
            return redirect('created', admin_id=progress.admin_id)
    else:
        form = ProgressCreateForm()

    return render(request, 'create_progress.html', {'form': form})
def created_view(request, admin_id):
    """Widok z linkami do panelu admina i podglądu"""
    try:
        progress = Progress.objects.get(admin_id=admin_id)
    except Progress.DoesNotExist:
        raise Http404("Progress bar not found")

    admin_link = f"/admin-panel/{progress.admin_id}/"
    public_link = f"/progress/{progress.public_id}/"

    return render(request, 'created.html', {
        'progress': progress,
        'admin_link': admin_link,
        'public_link': public_link,
    })


def delete_update(request, admin_id):
    """Funkcja do usuwania aktualizacji."""
    if request.method == 'POST':
        update_id = request.POST.get('update_id')
        try:
            update = Update.objects.get(id=update_id, progress__admin_id=admin_id)
            update.delete()
            return JsonResponse({'success': True})
        except Update.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Aktualizacja nie została znaleziona'})


def progress_embed_api(request, public_id):
    """API endpoint for embedding progress bar"""
    try:
        progress = Progress.objects.get(public_id=public_id)
        updates = progress.updates.all().order_by('-created_at')[:5]  # Ostatnie 5 aktualizacji

        data = {
            'name': progress.name,
            'percentage': progress.percentage,
            'updates': [
                {
                    'title': update.title,
                    'description': update.description,
                    'created_at': update.created_at.strftime("%Y-%m-%d %H:%M")
                } for update in updates
            ],
            'success': True
        }
        return JsonResponse(data)
    except Progress.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Progress bar not found'}, status=404)