from django.forms.widgets import TextInput


class CustomCaptchaWidget(TextInput):
    def __init__(self, attrs=None):
        attrs = {'class': 'form-control'} if attrs is None else attrs
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        attrs['class'] = attrs.get('class', '') + ' form-control'
        return super().render(name, value, attrs, renderer)