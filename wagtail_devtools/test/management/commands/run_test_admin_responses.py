
from typing import List
from django.core.management.base import BaseCommand
from django.urls import reverse
import requests
from dataclasses import dataclass, field


class Command(BaseCommand):
    def handle(self, *args, **options):
        host = "http://localhost:8000"
        index = requests.get(f"{host}{reverse('api_view')}")
        views = [view for view in index.json().get("api-views")]
        
        for view in views:
            response = requests.get(view).json()
            
            r = View(**response.get("meta"))
            results = response.get("results")

            for result in results:
                r.results.append(Result(**result))

            errors = r.get_error_500()
            import pprint
            pprint.pprint(errors)


@dataclass
class Result:
    title: None
    editor_url: None
    editor_status_code: None
    editor_status_text: None
    fe_url: None
    fe_status_code: None
    fe_status_text: None
    app_name: None
    class_name: None


@dataclass
class View:
    host: None
    fe_OK: None
    fe_500_ERROR: None
    fe_404_Response: None
    be_OK: None
    be_500_ERROR: None
    be_404_Response: None
    total_checks: None
    index: None
    results: List = field(default_factory=list)

    def get_error_500(self):
        return [result for result in self.results if result.fe_status_code == 500]


