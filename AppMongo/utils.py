from django.conf import settings


FLEX_FIELDS_OPTIONS = getattr(settings, "REST_FLEX_FIELDS", {})
EXPAND_PARAM = FLEX_FIELDS_OPTIONS.get("EXPAND_PARAM", "expand")
FIELDS_PARAM = FLEX_FIELDS_OPTIONS.get("FIELDS_PARAM", "fields")
OMIT_PARAM = FLEX_FIELDS_OPTIONS.get("OMIT_PARAM", "omit")


if "WILDCARD_EXPAND_VALUES" in FLEX_FIELDS_OPTIONS:
    WILDCARD_VALUES = FLEX_FIELDS_OPTIONS["WILDCARD_EXPAND_VALUES"]
elif "WILDCARD_VALUES" in FLEX_FIELDS_OPTIONS:
    WILDCARD_VALUES = FLEX_FIELDS_OPTIONS["WILDCARD_VALUES"]
else:
    WILDCARD_VALUES = ["~all", "*"]


def is_expanded(request, field: str) -> bool:
    expand_value = request.query_params.get(EXPAND_PARAM)
    expand_fields = []
    if expand_value:
        for f in expand_value.split(","):
            expand_fields.extend([_ for _ in f.split(".")])

    return "~all" in expand_fields or field in expand_fields