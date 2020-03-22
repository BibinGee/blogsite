from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.fields import RichTextField
from .models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    # desc = forms.CharField(widget=forms.Textarea, max_length=500, label='摘要', required=False)
    content = forms.CharField(widget=CKEditorUploadingWidget(config_name='body'), label='正文', required=True)
    # category = forms.ModelChoiceField(
    #     queryset=Category.objects.all(),
    #     widget=autocomplete.ModelSelect2(url='category-autocomplete'),
    #     label='分类',
    # )
    # tag = forms.ModelMultipleChoiceField(
    #     queryset=Tag.objects.all(),
    #     widget=autocomplete.ModelSelect2(url='tag-autocomplete'),
    #     label='标签'
    # )
    #
    class Meta:
        model = Post
        fields = ('category', 'tag', 'title', 'content', 'status')


