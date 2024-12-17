# clique_ratio_analysis/models.py
from django.db import models
from intake_form.models import Process


class CliqueRatioAnalysis(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    analysis_date = models.DateTimeField(auto_now_add=True)
    clique_ratio = models.FloatField()

    def __str__(self):
        return f"Clique Ratio Analysis for {self.process.name} on {self.analysis_date}"

    def calculate_clique_ratio(self):
        # Implement the logic to calculate the clique ratio for the process
        total_contributors = self.process.total_contributors
        total_steps = self.process.steps.count()
        if total_steps == 0:
            return 0
        return total_contributors / total_steps

    def save(self, *args, **kwargs):
        self.clique_ratio = self.calculate_clique_ratio()
        super().save(*args, **kwargs)
