def get_severity(behavior):

    mapping = {

        "opened_panel":
        "LOW",

        "walkway_violation":
        "MEDIUM",

        "unauthorized_intervention":
        "HIGH",

        "forklift_overload":
        "CRITICAL"
    }

    return mapping[behavior]