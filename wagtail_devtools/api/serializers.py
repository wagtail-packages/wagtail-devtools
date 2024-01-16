from django.urls import reverse

from wagtail_devtools.api.helpers import (
    get_backend_response,
    get_form_page_models,
    get_host,
    init_ret,
    results_item,
)


def form_types_serializer(request, session):
    ret = init_ret("Form types")

    for model in get_form_page_models():
        item = model.objects.first()

        editor_url = f"{get_host(request)}{reverse('wagtailforms:list_submissions', args=[item.id])}"
        be_response = get_backend_response(session, item, editor_url)

        ret["results"].append(
            results_item(
                request,
                None,
                None,
                be_response,
                defaults={
                    "title": item.title,
                    "editor_url": editor_url,
                    "editor_status_code": be_response.status_code,
                    "editor_status_text": be_response.reason,
                    "fe_url": None,
                    "fe_status_code": None,
                    "fe_status_text": None,
                    "app_name": None,
                    "class_name": None,
                },
            )
        )

    return ret
