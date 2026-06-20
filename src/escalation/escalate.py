def get_action(severity):

    if severity in [

        "LOW",
        "MEDIUM"

    ]:

        return "DB_LOG"

    else:

        return "ALERT + DB_LOG"