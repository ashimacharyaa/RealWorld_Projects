import cv2
import time
import numpy as np
from hand_tracker import HandTracker

PANEL_W      = 220       
PANEL_BG     = (30, 30, 30)     

# Colours
COL_UP       = (60, 220, 60)    
COL_DOWN     = (60, 60, 160)    
COL_TEXT     = (230, 230, 230)
COL_COUNT    = (80, 220, 255)   

FINGER_NAMES = ["Thumb", "Index", "Middle", "Ring", "Pinky"]


def draw_finger_diagram(panel: np.ndarray, finger_states: dict) -> None:
    h, w = panel.shape[:2]

    count = finger_states.get("count", 0)
    cv2.putText(panel, f"Fingers up: {count}", (12, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, COL_COUNT, 2, cv2.LINE_AA)

    palm_cx = w // 2
    palm_cy = h - 60
    palm_r  = 36
    cv2.circle(panel, (palm_cx, palm_cy), palm_r, (80, 80, 80), -1)
    cv2.circle(panel, (palm_cx, palm_cy), palm_r, (120, 120, 120), 2)

   
    num_fingers = len(FINGER_NAMES)
    spacing     = w // (num_fingers + 1)       
    bar_w       = 18
    bar_max_h   = palm_cy - 80                 
    bar_top_y   = palm_cy - palm_r - bar_max_h  

    height_ratios = [0.60, 0.90, 1.00, 0.88, 0.70]  

    for i, name in enumerate(FINGER_NAMES):
        cx       = spacing * (i + 1)
        ratio    = height_ratios[i]
        bar_h    = int(bar_max_h * ratio)
        top_y    = palm_cy - palm_r - bar_h + 6  
        colour   = COL_UP if finger_states.get(name, False) else COL_DOWN

        bx = cx - bar_w // 2
        cv2.rectangle(panel, (bx, top_y + bar_w // 2),
                      (bx + bar_w, palm_cy - palm_r + 6), colour, -1)

        cv2.circle(panel, (cx, top_y + bar_w // 2), bar_w // 2, colour, -1)

        label_y = max(top_y - 6, 50)
        cv2.putText(panel, name[0],           
                    (cx - 5, label_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                    COL_TEXT, 1, cv2.LINE_AA)

    cv2.rectangle(panel, (12, h - 36), (24, h - 26), COL_UP, -1)
    cv2.putText(panel, "Up",   (30, h - 27), cv2.FONT_HERSHEY_SIMPLEX,
                0.42, COL_TEXT, 1, cv2.LINE_AA)
    cv2.rectangle(panel, (72, h - 36), (84, h - 26), COL_DOWN, -1)
    cv2.putText(panel, "Down", (90, h - 27), cv2.FONT_HERSHEY_SIMPLEX,
                0.42, COL_TEXT, 1, cv2.LINE_AA)


def main():
 
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    tracker       = HandTracker(max_hands=2, detection_confidence=0.7,
                                tracking_confidence=0.7)
    previous_time = 0

    print("Hand tracking started. Press 'q' to quit.")

    # Main loop 
    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to read frame from webcam. Exiting.")
            break

        frame = cv2.flip(frame, 1)

        frame = tracker.find_hands(frame, draw=True)

        finger_states = tracker.count_fingers(frame, hand_index=0)

        current_time  = time.time()
        fps           = 1 / (current_time - previous_time) if previous_time else 0
        previous_time = current_time

        cv2.putText(frame, f"FPS: {int(fps)}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Hands: {tracker.num_hands_detected()}", (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#----------------------------------
        panel_h = frame.shape[0]
        panel   = np.full((panel_h, PANEL_W, 3), PANEL_BG, dtype=np.uint8)
        draw_finger_diagram(panel, finger_states)

        combined = np.hstack([frame, panel])

        cv2.imshow("Hand Tracking – press 'q' to quit", combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    tracker.close()


if __name__ == "__main__":
    main()