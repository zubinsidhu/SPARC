import cv2

def open():
    """Opens the default camera using OpenCV and displays the video feed. Press 'q' to exit."""

    return "Camera is open"

    global cap  # Access the global cap variable
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        cv2.imshow('Camera Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
