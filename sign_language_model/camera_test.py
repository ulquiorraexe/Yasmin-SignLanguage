import cv2


def test_camera():
    print("Starting camera test...")

    # Try all camera indices
    for i in range(3):
        print(f"\nTrying camera index {i}...")
        cap = cv2.VideoCapture(i)

        if not cap.isOpened():
            print(f"Camera {i} could not be opened")
            continue

        ret, frame = cap.read()
        if ret:
            print(f"Camera {i} is working!")
            print(f"Frame size: {frame.shape}")

            # Save test image
            cv2.imwrite(f"camera_{i}_test.jpg", frame)
            print(f"Test image saved as camera_{i}_test.jpg")
        else:
            print(f"Camera {i} cannot capture image")

        cap.release()

    print("\nCamera test completed.")


if __name__ == "__main__":
    test_camera()
