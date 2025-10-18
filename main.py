"""
Eye Tracking Camera Switcher - Main Application
Switches between cameras based on eye gaze direction.
"""

import cv2
import mediapipe as mp
import time

def main():
    """Main application function."""
    print("Eye Tracking Camera Switcher")
    print("=" * 40)
    print("Starting Simple Eye Camera Switcher...")

    # Initialize MediaPipe
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.3,
        min_tracking_confidence=0.3
    )

    # Try to open both cameras
    print("Opening cameras...")
    cap0 = cv2.VideoCapture(0)  # Front camera
    cap1 = cv2.VideoCapture(1)  # Webcam

    # Check which cameras work
    cameras = []
    if cap0.isOpened():
        ret, frame = cap0.read()
        if ret:
            cameras.append(("Camera 0 (Front)", cap0))
            print("✓ Camera 0 (Front) working")
        else:
            cap0.release()

    if cap1.isOpened():
        ret, frame = cap1.read()
        if ret:
            cameras.append(("Camera 1 (Webcam)", cap1))
            print("✓ Camera 1 (Webcam) working")
        else:
            cap1.release()

    if len(cameras) < 2:
        print("✗ Need at least 2 cameras to switch between them")
        print("Available cameras:", len(cameras))
        for cap in [cap0, cap1]:
            if cap:
                cap.release()
        return

    # Use front camera (camera 0) for eye tracking, webcam (camera 1) for display
    eye_camera = cameras[0][1]  # Front camera for eye tracking
    current_camera = 0  # Start with front camera
    last_switch_time = time.time()

    print("✓ Eye tracking camera:", cameras[0][0])
    print("✓ Display camera:", cameras[1][0])
    print("Press 'q' to quit")

    frame_count = 0
    gaze_counter = 0
    last_gaze_direction = "CENTER/RIGHT"
    
    try:
        while True:
            # Capture frame from eye tracking camera
            ret, frame = eye_camera.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame
            results = face_mesh.process(rgb_frame)
            
            # Check if face is detected
            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                h, w, _ = frame.shape
                
                # Get eye landmarks for gaze detection
                # Left eye landmarks
                left_eye_indices = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
                # Right eye landmarks  
                right_eye_indices = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
                
                # Iris landmarks
                left_iris_indices = [468, 469, 470, 471, 472]
                right_iris_indices = [473, 474, 475, 476, 477]
                
                # Eye corner landmarks
                left_eye_corners = [33, 133]
                right_eye_corners = [362, 263]
                
                try:
                    # Extract iris centers
                    left_iris_center = [0, 0]
                    right_iris_center = [0, 0]
                    
                    for idx in left_iris_indices:
                        landmark = face_landmarks.landmark[idx]
                        left_iris_center[0] += landmark.x * w
                        left_iris_center[1] += landmark.y * h
                    
                    for idx in right_iris_indices:
                        landmark = face_landmarks.landmark[idx]
                        right_iris_center[0] += landmark.x * w
                        right_iris_center[1] += landmark.y * h
                    
                    left_iris_center[0] = int(left_iris_center[0] / len(left_iris_indices))
                    left_iris_center[1] = int(left_iris_center[1] / len(left_iris_indices))
                    right_iris_center[0] = int(right_iris_center[0] / len(right_iris_indices))
                    right_iris_center[1] = int(right_iris_center[1] / len(right_iris_indices))
                    
                    # Extract eye corners
                    left_corners = []
                    right_corners = []
                    
                    for idx in left_eye_corners:
                        landmark = face_landmarks.landmark[idx]
                        left_corners.append([int(landmark.x * w), int(landmark.y * h)])
                    
                    for idx in right_eye_corners:
                        landmark = face_landmarks.landmark[idx]
                        right_corners.append([int(landmark.x * w), int(landmark.y * h)])
                    
                    # Calculate horizontal gaze ratio
                    left_horizontal_ratio = 0.5
                    right_horizontal_ratio = 0.5
                    
                    if len(left_corners) >= 2:
                        left_corner = min(left_corners, key=lambda p: p[0])
                        right_corner = max(left_corners, key=lambda p: p[0])
                        eye_width = right_corner[0] - left_corner[0]
                        if eye_width > 0:
                            iris_offset = left_iris_center[0] - left_corner[0]
                            left_horizontal_ratio = iris_offset / eye_width
                    
                    if len(right_corners) >= 2:
                        left_corner = min(right_corners, key=lambda p: p[0])
                        right_corner = max(right_corners, key=lambda p: p[0])
                        eye_width = right_corner[0] - left_corner[0]
                        if eye_width > 0:
                            iris_offset = right_iris_center[0] - left_corner[0]
                            right_horizontal_ratio = iris_offset / eye_width
                    
                    # Average the ratios
                    avg_horizontal_ratio = (left_horizontal_ratio + right_horizontal_ratio) / 2
                    
                    # Determine gaze direction
                    if avg_horizontal_ratio < 0.4:  # Looking left (more sensitive)
                        gaze_direction = "LEFT"
                        target_camera = 1  # Show webcam when looking left
                    else:  # Looking center/right
                        gaze_direction = "CENTER/RIGHT"
                        target_camera = 0  # Show front camera when looking center/right
                    
                    # Count stable gaze direction
                    if gaze_direction == last_gaze_direction:
                        gaze_counter += 1
                    else:
                        gaze_counter = 0
                        last_gaze_direction = gaze_direction
                    
                    # Switch camera if needed (only if gaze is stable for 10 frames)
                    current_time = time.time()
                    if (target_camera != current_camera and 
                        current_time - last_switch_time > 2.0 and 
                        gaze_counter > 10):  # Wait 2 seconds AND stable gaze for 10 frames
                        current_camera = target_camera
                        last_switch_time = current_time
                        gaze_counter = 0
                        print(f"SWITCHING TO {cameras[current_camera][0]} (Gaze: {gaze_direction}, Ratio: {avg_horizontal_ratio:.2f})")
                    
                    # Draw debug info
                    cv2.putText(frame, f"Gaze: {gaze_direction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f"Current Camera: {cameras[current_camera][0]}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(frame, f"Target Camera: {cameras[target_camera][0]}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(frame, f"Ratio: {avg_horizontal_ratio:.2f}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    
                    # Show if switching is needed
                    if target_camera != current_camera:
                        cv2.putText(frame, "SWITCHING NEEDED!", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    
                    # Draw iris centers
                    cv2.circle(frame, tuple(left_iris_center), 5, (0, 255, 0), -1)
                    cv2.circle(frame, tuple(right_iris_center), 5, (0, 255, 0), -1)
                    
                except Exception as e:
                    print(f"Error in gaze detection: {e}")
                    cv2.putText(frame, "FACE DETECTED - GAZE ERROR", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "NO FACE DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Display the frame from the current camera (not just eye tracking camera)
            if current_camera == 0:
                display_frame = frame  # Show front camera
            else:
                # Get frame from webcam
                ret_webcam, webcam_frame = cameras[1][1].read()
                if ret_webcam:
                    display_frame = webcam_frame
                else:
                    display_frame = frame  # Fallback to eye tracking camera
            
            # Add camera info to display frame
            cv2.putText(display_frame, f"ACTIVE CAMERA: {cameras[current_camera][0]}", (10, display_frame.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            cv2.imshow("Eye Tracking Camera Switcher", display_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    
    finally:
        # Clean up
        print("Cleaning up...")
        for _, cap in cameras:
            cap.release()
        cv2.destroyAllWindows()
        print("Done!")

if __name__ == "__main__":
    main()