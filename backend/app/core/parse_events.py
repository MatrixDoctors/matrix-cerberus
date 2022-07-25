from app.core.models import BotGlobalData, ExternalUrlData, RoomSpecificData, UserData


def parse_event_data(type: str, data):
    if type == f"external_url":
        return ExternalUrlData.parse_obj(data)

    elif type == "rooms":
        return RoomSpecificData.parse_obj(data)

    elif type == "user":
        return UserData.parse_obj(data)

    elif type == "global_data":
        return BotGlobalData.parse_obj(data)


def parse_event_type(type: str, app_name, **additional_type_data):
    if type == f"external_url":
        event_type = f"{app_name}.external_url"

    elif type == "rooms":
        event_type = f"{app_name}.rooms.{additional_type_data['room_id']}"

    elif type == "user":
        event_type = f"{app_name}.user.{additional_type_data['user_id']}"

    elif type == "global_data":
        event_type = f"{app_name}.global_data"

    return event_type
