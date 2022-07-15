from app.core.models import ExternalUrlData, RoomSpecificData


def parse_events(type: str, data, **additional_type_data):
    if type == "matrix-cerberus.external_url":
        return ExternalUrlData.parse_obj(data)
    elif type == f"matrix-cerberus.rooms.{additional_type_data['room_id']}":
        return RoomSpecificData.parse_obj(data)
