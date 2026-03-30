from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        friendly_messages = {
            401: "You are not authorized. Please login first.",
            403: "You do not have permission to perform this action.",
            404: "The requested resource was not found.",
            405: "This HTTP method is not allowed on this endpoint.",
        }

        if response.status_code in friendly_messages and "detail" not in response.data:
            response.data["detail"] = friendly_messages[response.status_code]

        if response.status_code == 401:
            code = response.data.get("code", "")
            if code == "token_not_valid":
                response.data = {
                    "detail": "Your session has expired. Please login again.",
                    "code": "token_not_valid",
                }

    return response
