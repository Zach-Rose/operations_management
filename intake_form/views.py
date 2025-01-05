from django.shortcuts import render, redirect
from .forms import ProcessForm, ProcessStepForm
from .models import Process, ProcessStep
from .process_analysis import analyze_process

def submit_process_form(request):
    if request.method == 'POST':
        process_form = ProcessForm(request.POST)
        if process_form.is_valid():
            process = process_form.save()
            steps_data = []
            step_index = 1
            while f'steps-{step_index}-name' in request.POST:
                step_data = {
                    'name': request.POST.get(f'steps-{step_index}-name'),
                    'duration_value': request.POST.get(f'steps-{step_index}-duration_value', '').strip(),
                    'duration_unit': request.POST.get(f'steps-{step_index}-duration_unit'),
                    'contributors': request.POST.get(f'steps-{step_index}-contributors')
                }
                steps_data.append(step_data)
                step_index += 1

            bottlenecks = None
            image_path = None
            if steps_data:
                steps_dict = {}
                for step_data in steps_data:
                    step_form = ProcessStepForm(step_data)
                    if step_form.is_valid():
                        step = step_form.save(commit=False)
                        step.process = process
                        step.save()
                        process.steps.add(step)
                        contributors_text = step_data.get('contributors', '')
                        contributors = [name.strip() for name in contributors_text.split(',')]
                        steps_dict[step.name] = contributors
                bottlenecks, image_path = analyze_process(steps_dict)

            if bottlenecks is not None:
                return render(request, 'intake_form/success.html',
                              {'clique_ratio': bottlenecks, 'image_path': image_path.replace('intake_form/static/', 'static/'), 'steps_data': steps_data})
            else:
                return render(request, 'intake_form/submit_form.html',
                              {'process_form': process_form, 'error': 'Invalid step data or no steps provided'})
    else:
        process_form = ProcessForm()
    return render(request, 'intake_form/submit_form.html', {'process_form': process_form})

def success_page(request):
    return render(request, 'intake_form/success.html')