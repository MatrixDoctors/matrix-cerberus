from app.core.models import ExternalUrlData


def parse_events(type: str, data):
    if type == "matrix-cerberus.external_url":
        return ExternalUrlData.parse_obj(data)
