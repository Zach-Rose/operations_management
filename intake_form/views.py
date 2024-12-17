from django.shortcuts import render, redirect
from .forms import ProcessForm, ProcessStepForm, ContributorForm
from .models import Process, ProcessStep, Contributor
from clique_ratio_analysis.analysis import perform_clique_ratio_analysis

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

            print(f"Steps data: {steps_data}")
            clique_ratio = None
            image_path = None
            all_contributors = []
            if steps_data:
                for step_data in steps_data:
                    print(f"Processing step data: {step_data}")
                    step_form = ProcessStepForm(step_data)
                    if step_form.is_valid():
                        step = step_form.save(commit=False)
                        step.process = process
                        step.save()
                        process.steps.add(step)
                        # Parse contributors
                        contributors_text = step_data.get('contributors', '')
                        contributors = [name.strip() for name in contributors_text.split(',')]
                        all_contributors.append(contributors)
                        print(f"Contributors: {contributors}")
                    else:
                        print(f"Step form is not valid: {step_form.errors}")
                # Perform clique-ratio analysis
                clique_ratio, image_path = perform_clique_ratio_analysis(all_contributors)
            else:
                print("No steps data provided")

            if clique_ratio is not None and image_path is not None:
                return render(request, 'intake_form/success.html',
                              {'clique_ratio': clique_ratio, 'image_path': image_path})
            else:
                return render(request, 'intake_form/submit_form.html',
                              {'process_form': process_form, 'error': 'Invalid step data or no steps provided'})
        else:
            print(f"Process form is not valid: {process_form.errors}")
    else:
        process_form = ProcessForm()
    return render(request, 'intake_form/submit_form.html', {'process_form': process_form})
def success_page(request):
    return render(request, 'intake_form/success.html')