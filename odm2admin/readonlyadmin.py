# adopted from http://gremu.net/blog/2010/django-admin-read-only-permission/
from django.contrib.gis import admin
from django.core.exceptions import PermissionDenied

from ajax_select.fields import autoselect_fields_check_can_add


class ReadOnlyAdmin(admin.OSMGeoAdmin):
    """ in order to get + popup functions subclass this or do
    the same hook inside of your get_form """

    def get_form(self, request, obj=None, **kwargs):
        form = super(ReadOnlyAdmin, self).get_form(request, obj, **kwargs)
        if 'featuregeometrywkt' in form.declared_fields and self.__user_is_readonly(request):
            form.declared_fields['featuregeometrywkt'].widget.attrs['readonly'] = True

        # This is commented since django ajax selects doesn't seem to work with it
        # autoselect_fields_check_can_add(form, self.model, request.user)

        return form

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
            elif 'duplicate_results_event' in actions:
                del actions['duplicate_results_event']

        return actions

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if self.__user_is_readonly(request):
            self.save_as = False
            self.readonly_fields = self.user_readonly
            self.inlines = self.user_readonly_inlines

            extra_context = extra_context or {}
            extra_context['show_save'] = False
            extra_context['show_save_as_new'] = False
            extra_context['show_save_and_continue'] = False

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
            self.readonly_fields = list()
            self.form = self.form
            self.inlines = self.inlines_list
            request.readonly = False
            return super(ReadOnlyAdmin, self).change_view(
                request, object_id, form_url, extra_context=extra_context)

    @staticmethod
    def __user_is_readonly(request):
        groups = [x.name for x in request.user.groups.all()]
        return "readonly" in groups
