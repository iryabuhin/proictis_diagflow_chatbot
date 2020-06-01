from app.intent_handlers import mentor_info
from app.intent_handlers import project_info

INTENT_HANDLER = {
    'info_mentor_name_query': mentor_info.get_mentor_info,
    'projects_info_name_query': project_info.get_project_info,
    'all_projects_info_trigger_followup_event': project_info.call_followup_event,
    'all_projects_info_event_response': project_info.get_all_projects_info
}
