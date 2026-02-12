import cv2
import numpy as np

def process_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Noise reduction
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold
    _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    total_objects = len(contours)
    areas = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 50:  # ignore noise
            areas.append(area)
            cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)

    # Save annotated image
    output_path = image_path.replace(".jpg", "_processed.jpg")
    cv2.imwrite(output_path, image)

    return {
        "total_objects": total_objects,
        "areas": areas,
        "average_area": np.mean(areas) if areas else 0,
        "processed_image": output_path
    }
