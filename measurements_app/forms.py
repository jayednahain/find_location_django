from django import forms
from .models import Measurement

class MeasuremntForms(forms.ModelForm):
   class Meta:
      model = Measurement
      fields =['destination',] #only user destination form whare we want o go or mesure the distance