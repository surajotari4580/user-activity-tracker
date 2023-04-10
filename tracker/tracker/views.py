import logging
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError
from .models import Activity_tracker_logs, READ, CREATE, UPDATE, DELETE, SUCCESS, FAILED

class ActivityTracker:
    log_message = None
    
    def _get_action_type(self, request) -> str:
        return self.action_type_mapper().get(f"{request.method.upper()}")
    
    def _build_log_message(self, request) -> str:
        return self.log_message
    
    @staticmethod
    def action_type_mapper():
        return {
            "GET" : READ,
            "POST" : CREATE,
            "PUT" : UPDATE,
            "PATCH" : UPDATE,
            "DELETE" : DELETE,
        }
        
    @staticmethod
    def _get_user(request):
        return request.user if request.user.is_authenticated() else None
    
    def write_log(self, request, response):
        status = SUCCESS if response.status_code < 400 else FAILED
        member = self._get_user(request)
        
        if member and not getattr(settings, "TESTING", False):
            logging.info("Started log entry")
            
            data = {
                "member": member,
                "action_type":self._get_action_type(request),
                "status": status,
                "remark": self.get_log_message(request),
            }
            
            try:
                data["content_type"] = ContentType.objects.get_for_model(
                    self.get_queryset().model
                )
                data["content_object"] = self.get_object()
            except (AttributeError, ValidationError):
                data["content_type"] = None
            except AssertionError:
                pass
            
            Activity_tracker_logs.objects.create(**data)
            
    def final_response(self, request, *args, **kwargs):
        response = super().finalize_response(request, *args, **kwargs)
        self._write_log(request, response)
        return response