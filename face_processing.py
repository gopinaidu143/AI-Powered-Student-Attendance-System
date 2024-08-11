import cv2

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def detect_face(image_path):

    image = cv2.imread(image_path)

    # Resize the image
    resized_image = cv2.resize(image, (300, 300))  # Adjust the size as needed

    # Convert to grayscale
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        print("No faces detected")
        return None

    # Get the largest face (assuming the first face is the largest)
    (x, y, w, h) = faces[0]

    # Define padding around the detected face (adjust as needed)
    padding = 20

    # Calculate the coordinates for cropping with padding around the face
    top = max(0, y - padding)
    bottom = min(resized_image.shape[0], y + h + padding)
    left = max(0, x - padding)
    right = min(resized_image.shape[1], x + w + padding)

    # Crop the image with padding around the face
    cropped_face_with_padding = resized_image[top:bottom, left:right]

    # Resize the cropped face to 216x216
    resized_face = cv2.resize(cropped_face_with_padding, (216, 216))
    if resized_face is not None:
        # Display the cropped face
        cv2.imshow("Cropped Face", resized_face)
          # Specify the output path and filename
        cv2.imwrite(image_path, resized_face)
        print(f"Saved cropped face to: {image_path}")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No face detected in the image")


    return resized_face
