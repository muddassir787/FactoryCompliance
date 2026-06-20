import uuid
import json
from datetime import datetime

def create_report(

    clip_id,
    behavior,
    severity

):

    report = {

        "event_id":
        str(uuid.uuid4()),

        "timestamp":
        datetime.now().isoformat(),

        "clip_id":
        clip_id,

        "zone":
        "Zone-1",

        "behavior_class":
        behavior,

        "policy_rule_ref":
        "3.3.2",

        "event_description":
        f"{behavior} detected",

        "severity":
        severity,

        "escalation_action":
        "DB_LOG"

    }

    with open(

        f"outputs/reports/{report['event_id']}.json",

        "w"

    ) as f:

        json.dump(
            report,
            f,
            indent=4
        )

    return report