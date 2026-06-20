from ultralytics import YOLO

model = YOLO("yolo11n.pt")

def detect_people(frame):

    results = model(frame)

    persons = []

    for result in results:

        boxes = result.boxes

        for box in boxes:

            cls = int(box.cls)

            if cls == 0:

                x1,y1,x2,y2 = map(
                    int,
                    box.xyxy[0]
                )

                persons.append(
                    (x1,y1,x2,y2)
                )

    return persons