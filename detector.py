import cv2
import numpy as np
from ultralytics import YOLO
from shapely.geometry import Point, Polygon

CLASSES = {0: "person", 2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}
FENCE_ZONE = Polygon([(300, 100), (900, 100), (900, 600), (300, 600)])

class Detector:
    def __init__(self, model_path="models/yolov8n.pt"):
        self.model = YOLO(model_path)
        self.inside_zone_ids = set()

    @staticmethod
    def is_night(frame):
        return np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)) < 60

    def process(self, frame):
        alerts = []
        night = self.is_night(frame)
        if night:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(cv2.createCLAHE(3.0, (8, 8)).apply(gray), cv2.COLOR_GRAY2BGR)

        results = self.model.track(frame, persist=True, classes=list(CLASSES.keys()),
                                    tracker="bytetrack.yaml", verbose=False)[0]

        cv2.polylines(frame, [np.array(FENCE_ZONE.exterior.coords, np.int32)], True, (0, 0, 255), 2)

        if results.boxes.id is not None:
            for box, tid, cls in zip(results.boxes.xyxy.cpu().numpy(),
                                      results.boxes.id.cpu().numpy(),
                                      results.boxes.cls.cpu().numpy()):
                x1, y1, x2, y2 = box.astype(int)
                tid, cls = int(tid), int(cls)
                label = CLASSES.get(cls, "obj")
                cx, cy = (x1 + x2) // 2, y2
                color = (0, 255, 0)

                inside = FENCE_ZONE.contains(Point(cx, cy))
                if label == "person" and inside and tid not in self.inside_zone_ids:
                    self.inside_zone_ids.add(tid)
                    color = (0, 0, 255)
                    alerts.append({"type": "FENCE_INTRUSION", "track_id": tid,
                                   "class": label, "night": night, "confidence": 1.0})
                elif not inside and tid in self.inside_zone_ids:
                    self.inside_zone_ids.discard(tid)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{label}#{tid}", (x1, y1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return frame, alerts, night