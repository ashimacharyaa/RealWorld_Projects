import cv2
import mediapipe as mp



FINGER_TIPS = {
    "Thumb":  (4, 3),  
    "Index":  (8, 6),
    "Middle": (12, 10),
    "Ring":   (16, 14),
    "Pinky":  (20, 18),
}

FINGER_ORDER = ["Thumb", "Index", "Middle", "Ring", "Pinky"]


class HandTracker:
    def __init__(self, max_hands=2, detection_confidence=0.7, tracking_confidence=0.7):
       
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,       
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.results = None

    def find_hands(self, frame, draw=True):
       
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(rgb_frame)

        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,                                 
                    hand_landmarks,                        
                    self.mp_hands.HAND_CONNECTIONS,          
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style(),
                )

        return frame

    def get_landmark_positions(self, frame, hand_index=0):
       
        landmark_list = []

        if self.results and self.results.multi_hand_landmarks:
            if hand_index < len(self.results.multi_hand_landmarks):
                hand = self.results.multi_hand_landmarks[hand_index]
                height, width, _ = frame.shape

                for idx, landmark in enumerate(hand.landmark):
                    pixel_x = int(landmark.x * width)
                    pixel_y = int(landmark.y * height)
                    landmark_list.append([idx, pixel_x, pixel_y])

        return landmark_list

    def count_fingers(self, frame, hand_index=0):
       
        landmarks = self.get_landmark_positions(frame, hand_index)
        result = {name: False for name in FINGER_ORDER}
        result["count"] = 0

        if not landmarks:
            return result

        lm = {lm_id: (x, y) for lm_id, x, y in landmarks}

        for finger_name in FINGER_ORDER:
            tip_id, base_id = FINGER_TIPS[finger_name]

            if tip_id not in lm or base_id not in lm:
                continue

            tip_x, tip_y = lm[tip_id]
            base_x, base_y = lm[base_id]

            if finger_name == "Thumb":
                is_up = tip_x > base_x
            else:
                is_up = tip_y < base_y

            result[finger_name] = is_up
            if is_up:
                result["count"] += 1

        return result

    def num_hands_detected(self):
        if self.results and self.results.multi_hand_landmarks:
            return len(self.results.multi_hand_landmarks)
        return 0

    def close(self):
        self.hands.close()