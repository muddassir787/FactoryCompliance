import cv2
import numpy as np
from datetime import datetime

from src.detection.video_reader import read_video
from src.detection.person_detector import detect_people

from src.severity.severity import get_severity
from src.escalation.escalate import get_action

from src.reports.report import create_report

from database.db import init_db, insert_violation


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

VIDEO_PATH = "data/sample.mp4"

# Polygon Safe Walkway Coordinates
# Modify these points according to your camera view

SAFE_ZONE = np.array([
    (470, 50),    # Top Left
    (600, 50),    # Top Right
    (800, 500),  # Bottom Right
    (580, 450)    # Bottom Left
], np.int32)

processed_positions = set()


# --------------------------------------------------
# CHECK WALKWAY VIOLATION
# --------------------------------------------------

def check_walkway_violation(person_box):

    x1, y1, x2, y2 = person_box

    # Use feet position instead of center
    foot_x = (x1 + x2) // 2
    foot_y = y2

    point = (foot_x, foot_y)

    result = cv2.pointPolygonTest(
        SAFE_ZONE,
        point,
        False
    )

    # Inside polygon = Safe
    # Outside polygon = Violation
    return result < 0


# --------------------------------------------------
# PROCESS VIDEO
# --------------------------------------------------

def process_video(video_path):

    print("\nStarting Video Processing...\n")

    frame_count = 0
    total_violations = 0

    for frame in read_video(video_path):

        frame_count += 1

        persons = detect_people(frame)

        print(
            f"Frame {frame_count} | Persons Detected: {len(persons)}"
        )

        for person in persons:

            x1, y1, x2, y2 = person

            foot_x = (x1 + x2) // 2
            foot_y = y2

            violation = check_walkway_violation(person)

            if violation:

                # Avoid duplicate alerts
                position_key = (
                    foot_x // 50,
                    foot_y // 50
                )

                if position_key in processed_positions:
                    continue

                processed_positions.add(position_key)

                total_violations += 1

                behavior = "walkway_violation"

                severity = get_severity(
                    behavior
                )

                action = get_action(
                    severity
                )

                report = create_report(
                    clip_id=video_path,
                    behavior=behavior,
                    severity=severity
                )

                insert_violation(report)

                print("\nViolation Detected")

                print(
                    f"Behavior : {behavior}"
                )

                print(
                    f"Severity : {severity}"
                )

                print(
                    f"Action   : {action}"
                )

                print(
                    f"Report ID: {report['event_id']}"
                )

                # Red Bounding Box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 255),
                    2
                )

                cv2.circle(
                    frame,
                    (foot_x, foot_y),
                    5,
                    (0, 0, 255),
                    -1
                )

                cv2.putText(
                    frame,
                    severity,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2
                )

            else:

                # Green Bounding Box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.circle(
                    frame,
                    (foot_x, foot_y),
                    5,
                    (0, 255, 0),
                    -1
                )

        # --------------------------------------------------
        # DRAW SAFE WALKWAY POLYGON
        # --------------------------------------------------

        cv2.polylines(
            frame,
            [SAFE_ZONE],
            isClosed=True,
            color=(255, 0, 0),
            thickness=3
        )

        cv2.putText(
            frame,
            "SAFE WALKWAY",
            tuple(SAFE_ZONE[0]),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
            2
        )

        # Optional: Fill polygon with transparent overlay

        overlay = frame.copy()

        cv2.fillPoly(
            overlay,
            [SAFE_ZONE],
            (255, 0, 0)
        )

        alpha = 0.15

        frame = cv2.addWeighted(
            overlay,
            alpha,
            frame,
            1 - alpha,
            0
        )

        # --------------------------------------------------
        # DISPLAY
        # --------------------------------------------------

        cv2.imshow(
            "Factory Compliance Monitoring",
            frame
        )

        key = cv2.waitKey(1)

        if key == 27:
            break

    cv2.destroyAllWindows()

    print("\nProcessing Completed.")

    print(
        f"Total Violations: {total_violations}"
    )


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    init_db()

    start_time = datetime.now()

    print(
        f"Started at: {start_time}"
    )

    process_video(VIDEO_PATH)

    end_time = datetime.now()

    print(
        f"Finished at: {end_time}"
    )

    print(
        f"Duration: {end_time - start_time}"
    )