import cv2
import numpy as np

def process_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 1: Blur
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # Step 2: Otsu threshold
    _, thresh = cv2.threshold(
        blur, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Step 3: Morphological cleaning
    kernel = np.ones((5,5), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)

    # Step 4: Find contours
    contours, _ = cv2.findContours(
        cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    valid_contours = []
    areas = []

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if 100 < area < 8000:
            valid_contours.append(cnt)
            areas.append(area)
            cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)
            
            # (x, y), radius = cv2.minEnclosingCircle(cnt)
            # center = (int(x), int(y))
            # radius = int(radius)
            # cv2.circle(image, center, radius, (0,255,0), 2)

    output_path = image_path.replace(".jpg", "_processed.jpg")
    cv2.imwrite(output_path, image)

    return {
        "total_objects": len(valid_contours),
        "areas": areas,
        "average_area": np.mean(areas) if areas else 0,
        "median_area": np.median(areas) if areas else 0,
        "processed_image": output_path
    }