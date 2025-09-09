
import cv2
import mediapipe as mp
import pyautogui
import threading
import numpy as np

eye_control_active = False
smoothing_factor = 0.7  # Adjust for smoother cursor movement
sensitivity = 0.9  # Adjust cursor movement sensitivity
prev_x, prev_y = 0, 0  # For smoothing cursor movement

def eye_controlled_mouse():
    global eye_control_active, prev_x, prev_y
    
    eye_control_active = True
    print("Eye control is now activated. Press 'C' to Close Eye control")
    
    # Initialize the webcam and FaceMesh model
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()
    
    # Initialize reference point (when the eye is centered)
    ref_point = None
    calibration_time = 30  # frames to calibrate center position
    calibration_count = 0
    center_points = []

    while True:
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape

        if landmark_points:
            landmarks = landmark_points[0].landmark
            
            # Get eye landmarks (using both eyes for better stability)
            left_eye = landmarks[33]
            right_eye = landmarks[263]
            
            # Calculate center point between eyes
            eye_center_x = (left_eye.x + right_eye.x) / 2
            eye_center_y = (left_eye.y + right_eye.y) / 2
            
            # Calibration phase - first few frames to establish center reference
            if calibration_count < calibration_time:
                center_points.append((eye_center_x, eye_center_y))
                calibration_count += 1
                cv2.putText(frame, f"Calibrating... {calibration_count}/{calibration_time}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                if ref_point is None:
                    # Calculate average center position after calibration
                    ref_point = np.mean(center_points, axis=0)
                    print(f"Calibration complete. Reference point: {ref_point}")
                
                # Calculate relative movement from reference point
                dx = (eye_center_x - ref_point[0]) * sensitivity
                dy = (eye_center_y - ref_point[1]) * sensitivity
                
                # Get current mouse position
                current_x, current_y = pyautogui.position()
                
                # Calculate new position with smoothing
                new_x = current_x + dx * screen_w
                new_y = current_y + dy * screen_h
                
                # Apply smoothing
                new_x = prev_x * smoothing_factor + new_x * (1 - smoothing_factor)
                new_y = prev_y * smoothing_factor + new_y * (1 - smoothing_factor)
                
                # Ensure new position stays within screen bounds
                new_x = max(0, min(screen_w, new_x))
                new_y = max(0, min(screen_h, new_y))
                
                # Move mouse
                pyautogui.moveTo(new_x, new_y)
                prev_x, prev_y = new_x, new_y

            # Improved blink detection for clicking 
            left_eye_top = landmarks[145]
            left_eye_bottom = landmarks[159]
            top_y = int(left_eye_top.y * frame_h)
            bottom_y = int(left_eye_bottom.y * frame_h)

            # Blink threshold based on frame height 
            if abs(top_y - bottom_y) < frame_h * 0.01:
                pyautogui.click()
                pyautogui.sleep(1)

            # Visual feedback for eyes
            for landmark in [left_eye_top, left_eye_bottom]:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

        cv2.imshow('Eye Controlled Mouse', frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break

    cam.release()
    cv2.destroyAllWindows()
    eye_control_active = False

def start_eye_control_thread():
    global eye_control_active
    if not eye_control_active:
        eye_control_thread = threading.Thread(target=eye_controlled_mouse)
        eye_control_thread.daemon = True
        eye_control_thread.start()
        print("Eye control thread started.")
    else:
        print("Eye control is already running.")

if __name__ == "__main__":
    start_eye_control_thread()