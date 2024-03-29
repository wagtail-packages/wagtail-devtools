from django.urls import reverse

from wagtail_devtools.management.commands._base_admin_responses import (
    BaseAdminResponsesCommand,
)


class Command(BaseAdminResponsesCommand):
    def get_reports(self, *args, **options):
        session = self._log_in(options)

        return [
            {
                # PAGES EDIT
                "function": self.report_pages,
                "args": [session, options],
            },
            {
                # DASHBOARD
                "function": self.report_admin_list_pages,
                "args": [
                    session,
                    "DASHBOARD",
                    f"{options['host']}{reverse('wagtailadmin_home')}",
                ],
            },
            {
                # PAGES LIST
                "function": self.report_admin_list_pages,
                "args": [
                    session,
                    "PAGES list",
                    f"{options['host']}{reverse('wagtailadmin_explore_root')}",
                ],
            },
            {
                # SEARCH PAGES
                "function": self.report_admin_list_pages,
                "args": [
                    session,
                    "SEARCH all",
                    f"{options['host']}{reverse('wagtailadmin_pages:search')}",
                ],
            },
            {
                # AGING PAGES
                "function": self.report_admin_list_pages,
                "args": [
                    session,
                    "AGING PAGES list",
                    f"{options['host']}{reverse('wagtailadmin_reports:aging_pages')}",
                ],
            },
            {
                # COLLECTIONS
                "function": self.report_admin_list_pages,
                "args": [
                    session,
                    "COLLECTIONS list",
                    f"{options['host']}{reverse('wagtailadmin_collections:index')}",
                ],
            },
            {
                # DOCUMENTS LIST
                "function": self.report_admin_list_pages,
                "args": [
                    session,
                    "DOCUMENTS list",
                    f"{options['host']}{reverse('wagtaildocs:index')}",
                ],
            },
            {
                # GROUPS
                "function": self.report_admin_list_pages,
                "args": [
                    session,
                    "GROUPS list",
                    f"{options['host']}{reverse('wagtailusers_groups:index')}",
                ],
            },
            {
                # IMAGES LIST
                "function": self.report_admin_list_pages,
                "args": [
                    session,
                    "IMAGES list",
                    f"{options['host']}{reverse('wagtailimages:index')}",
                ],
            },
            {
                # LOCKED PAGES
                "function": self.report_admin_list_pages,
                "args": [
                    session,
                    "LOCKED PAGES list",
                    f"{options['host']}{reverse('wagtailadmin_reports:locked_pages')}",
                ],
            },
            {
                # REDIRECTS
                "function": self.report_admin_list_pages,
                "args": [
                    session,
                    "REDIRECTS list",
                    f"{options['host']}{reverse('wagtailredirects:index')}",
                ],
            },
            {
                # SITES
                "function": self.report_admin_list_pages,
                "args": [
                    session,
                    "SITES list",
                    f"{options['host']}{reverse('wagtailsites:index')}",
                ],
            },
            {
                # SITE HISTORY
                "function": self.report_admin_list_pages,
                "args": [
                    session,
                    "SITE HISTORY list",
                    f"{options['host']}{reverse('wagtailadmin_reports:site_history')}",
                ],
            },
            {
                # SNIPPETS LIST
                "function": self.report_admin_list_pages,
                "args": [
                    session,
                    "SNIPPETS list",
                    f"{options['host']}{reverse('wagtailsnippets:index')}",
                ],
            },
            {
                # USERS
                "function": self.report_admin_list_pages,
                "args": [
                    session,
                    "USERS list",
                    f"{options['host']}{reverse('wagtailusers_users:index')}",
                ],
            },
            {
                # WORKFLOWS LIST
                "function": self.report_admin_list_pages,
                "args": [
                    session,
                    "WORKFLOWS list",
                    f"{options['host']}{reverse('wagtailadmin_workflows:index')}",
                ],
            },
            {
                # WORKFLOWS TASKS
                "function": self.report_admin_list_pages,
                "args": [
                    session,
                    "WORKFLOWS TASKS list",
                    f"{options['host']}{reverse('wagtailadmin_workflows:task_index')}",
                ],
            },
            {
                # COLLECTIONS EDIT
                "function": self.report_collections,
                "args": [session, options],
            },
            {
                # DOCUMENTS
                "function": self.report_documents,
                "args": [session, options],
            },
            {
                # GROUPS EDIT
                "function": self.report_groups,
                "args": [session, options],
            },
            {
                # IMAGES
                "function": self.report_images,
                "args": [session, options],
            },
            {
                # REDIRECTS EDIT
                "function": self.report_admin_app_model,
                "args": [
                    session,
                    options,
                    "REDIRECTS edit",
                    "wagtailredirects",
                    "Redirect",
                ],
            },
            {
                # SETTINGS
                "function": self.report_settings_models,
                "args": [session, options],
            },
            {
                # SITES EDIT
                "function": self.report_sites,
                "args": [session, options],
            },
            {
                # SNIPPETS
                "function": self.report_snippets,
                "args": [session, options],
            },
            {
                # USERS EDIT
                "function": self.report_users,
                "args": [session, options],
            },
            {
                # WORKFLOWS EDIT
                "function": self.report_admin_app_model,
                "args": [
                    session,
                    options,
                    "WORKFLOWS edit",
                    "wagtailcore",
                    "Workflow",
                ],
            },
            {
                # WORKFLOWS TASK EDIT
                "function": self.report_admin_app_model,
                "args": [
                    session,
                    options,
                    "WORKFLOWS TASK edit",
                    "wagtailcore",
                    "Task",
                ],
            },
            {
                # MODELADMIN
                "function": self.report_model_admin,
                "args": [
                    session,
                    options,
                    [
                        "wagtail_devtools_test.TestModelAdminOne",
                        "wagtail_devtools_test.TestModelAdminTwo",
                        "wagtail_devtools_test.TestModelAdminThree",
                    ],
                ],
            },
        ]
