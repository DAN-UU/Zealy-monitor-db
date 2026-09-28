from monitor import check_once


def handler(request):
    try:
        result = check_once()
        return {"statusCode": 200, "body": result}
    except Exception as exc:
        return {"statusCode": 500, "body": {"status": "error", "error": str(exc)}}
