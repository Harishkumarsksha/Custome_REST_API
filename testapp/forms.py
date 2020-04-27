from django import forms

from testapp.models import Employee


class EmployeeForm(forms.ModelForm):
    # perfomer the form validation in the forms
    def clean_esal(self):

        inputsal = self.cleaned_data['esal']
        if int(inputsal) < 5000:
            raise forms.ValidationError(
                'The minimum Salary should be greater than 5000')
        return inputsal

    class Meta:

        model = Employee

        fields = '__all__'
