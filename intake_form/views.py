import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ProcessForm, ProcessStepForm
from .models import Process, ProcessStep
from .process_analysis import analyze_process
from clique_ratio_analysis.analysis import perform_clique_ratio_analysis

logger = logging.getLogger(__name__)


def index(request):
    process_form = ProcessForm()
    step_form = ProcessStepForm()
    return render(request, 'intake_form/submit_form.html', {'process_form': process_form, 'step_form': step_form})


def submit_process_form(request):
    try:
        if request.method == 'POST':
            logger.info(f"Request POST data: {request.POST}")
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

                    logger.info(f"Steps dictionary: {steps_dict}")

                    if steps_dict:
                        bottlenecks, image_path, nodes, edges = analyze_process(steps_dict)
                        return JsonResponse({
                            'clique_ratio': bottlenecks,
                            'image_path': image_path.replace('intake_form/static/', 'static/'),
                            'steps_data': steps_data,
                            'nodes': nodes,
                            'edges': edges
                        })
                    else:
                        logger.error('Steps dictionary is empty')
                        return JsonResponse({'error': 'Steps dictionary is empty'}, status=400)
                else:
                    logger.error('Invalid step data or no steps provided')
                    return JsonResponse({'error': 'Invalid step data or no steps provided'}, status=400)
            else:
                logger.error('Invalid form submission')
                return JsonResponse({'error': 'Invalid form submission'}, status=400)
    except Exception as e:
        logger.error(f"Error processing form submission: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


def success_page(request):
    return render(request, 'success.html')
