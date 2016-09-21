## adopted from http://gremu.net/blog/2010/django-admin-read-only-permission/
from django.contrib.gis import admin
from django.core.exceptions import PermissionDenied


class ReadOnlyAdmin(admin.ModelAdmin):
    """
    """

    def has_add_permission(self, request, obj=None):
        """

        Arguments:
        - `request`:
        - `obj`:
        """
        return not self.__user_is_readonly(request)

    def has_delete_permission(self, request, obj=None):
        """

        Arguments:
        - `request`:
        - `obj`:
        """
        return not self.__user_is_readonly(request)

    def get_actions(self, request):

        actions = super(ReadOnlyAdmin, self).get_actions(request)

        if self.__user_is_readonly(request):
            if 'delete_selected' in actions:
                del actions['delete_selected']

        return actions

    def change_view(self, request, object_id, form_url = '', extra_context=None):
        print request
        if self.__user_is_readonly(request):
            print self.__user_is_readonly(request)
            print "Readonly"
            self.readonly_fields = self.user_readonly
            self.inlines = self.user_readonly_inlines

            try:
                return super(ReadOnlyAdmin, self).change_view(
                    request, object_id, extra_context=extra_context)
            except PermissionDenied:
                pass

            if request.method == 'POST':
                raise PermissionDenied
            request.readonly = True
            return super(ReadOnlyAdmin, self).change_view(
                request, object_id, form_url, extra_context=extra_context)
        else:
            print self.__user_is_readonly(request)
            print "Admin"
            self.readonly_fields = []
            self.form = self.form
            self.inlines = self.inlines_list
            request.readonly = False
            return super(ReadOnlyAdmin, self).change_view(
                request, object_id, form_url, extra_context=extra_context)


    def __user_is_readonly(self, request):
        groups = [x.name for x in request.user.groups.all()]
        return "readonly" in groups
