from django.forms import ModelForm, Textarea, CharField, TextInput, ModelMultipleChoiceField, CheckboxSelectMultiple, HiddenInput
from .models import Post, Category, Author
from django.forms import ModelChoiceField


class PostForm(ModelForm):
    name = CharField(label='Post Name', widget=TextInput(attrs={'size': 40}))
    text = CharField(label='Enter Text', widget=Textarea(attrs={'rows': 10, 'cols': 60}))
    category = ModelMultipleChoiceField(queryset=Category.objects.all(), widget=CheckboxSelectMultiple)
    author = ModelChoiceField(queryset=Author.objects.all(), initial=Author.objects.get(user__username='Igor'), widget=HiddenInput)

    class Meta:
        model = Post
        fields = ['name', 'type', 'category', 'text', 'author']





