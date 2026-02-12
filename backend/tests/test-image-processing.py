from app.image_processing import process_image

def test_processing():
    result = process_image("sample.jpg")
    assert result["total_objects"] >= 0
