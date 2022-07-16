from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['commenting_user'].widget.attrs.update({'class': 'text-test'})
        self.fields['description'].widget.attrs.update({'class': 'text-test'})
        self.fields['user_rate'].widget.attrs.update({'style': "color:red;"})

    class Meta:
        model = Comment
        fields = ["commenting_user","description", "user_rate"]

        labels = {
            "commenting_user": "نام ",
            "user_rate": "امتیاز شما",
            "description": "نقد و بررسی شما ",
            "email":"ایمیل "


        }
        help_texts = {
            "rate": " امتیازاین کالا را وارد کن"
        }

        error_messages = {
            "rate": {
                "max_value": "عدد بیشتر از  5 ممنوعه",
                "min_value": "عدد کمتر از صفر ممنوعه",
            },
        }


