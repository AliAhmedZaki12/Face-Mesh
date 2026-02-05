import cv2
import mediapipe as mp

# MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# تخصيص شكل الـ Mesh
green_mesh = mp_drawing.DrawingSpec(
    color=(0, 255, 0),   # Green color
    thickness=1,         # Fine lines
    circle_radius=1      # small radius (porosity)
)

# Camera setup
cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh:

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # تحويل BGR → RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        # رسم الـ Mesh
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=green_mesh,
                    connection_drawing_spec=green_mesh
                )

        cv2.imshow("Green 3D Face Mesh", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC للخروج
            break

cap.release()
cv2.destroyAllWindows()
