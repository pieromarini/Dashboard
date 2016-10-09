from django.contrib import admin
from dashby.models import Document

#Admin page allowed_users modification.
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('uploaded_by', 'file')
    fields = ('id', 'uploaded_at', 'extension', 'thumbnail',
              'is_public', 'uploaded_by', 'allowed_users')
    filter_horizontal = ('allowed_users',)

    readonly_fields = ('id','uploaded_at')

admin.site.register(Document, DocumentAdmin)
