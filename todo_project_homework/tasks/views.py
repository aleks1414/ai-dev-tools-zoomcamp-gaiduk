from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.utils import timezone

def task_list(request):
	tasks = Task.objects.all().order_by('-created_at')
	return render(request, 'tasks/task_list.html', {'tasks': tasks})

def task_create(request):
	if request.method == 'POST':
		title = request.POST.get('title')
		description = request.POST.get('description')
		due_date = request.POST.get('due_date')
		if due_date == '':
			due_date = None
		task = Task(title=title, description=description, due_date=due_date)
		task.save()
		return redirect('task_list')
	return render(request, 'tasks/task_form.html')

def task_edit(request, pk):
	task = get_object_or_404(Task, pk=pk)
	if request.method == 'POST':
		task.title = request.POST.get('title')
		task.description = request.POST.get('description')
		due_date = request.POST.get('due_date')
		if due_date == '':
			task.due_date = None
		else:
			task.due_date = due_date
		task.save()
		return redirect('task_list')
	return render(request, 'tasks/task_form.html', {'task': task})

def task_delete(request, pk):
	task = get_object_or_404(Task, pk=pk)
	if request.method == 'POST':
		task.delete()
		return redirect('task_list')
	return render(request, 'tasks/task_confirm_delete.html', {'task': task})

def task_complete(request, pk):
	task = get_object_or_404(Task, pk=pk)
	task.completed = True
	task.save()
	return redirect('task_list')
