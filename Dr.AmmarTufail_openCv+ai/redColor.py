import cv2
import numpy as np

def get_background(cap, frames=60):
    """Capture a stable background frame."""
    bg = None
    for _ in range(frames):
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)  # mirror for a natural webcam feel
        bg = frame
    return bg

def get_color_bounds(color):
    """Return HSV bounds for the selected color."""
    color_bounds = {
        'red': [(0, 120, 70), (10, 255, 255), (170, 120, 70), (180, 255, 255)],
        'blue': [(100, 100, 70), (130, 255, 255)],
        'green': [(40, 100, 70), (80, 255, 255)],
        'yellow': [(20, 100, 70), (35, 255, 255)],
        'black': [(0, 0, 0), (180, 255, 30)]
    }
    return color_bounds.get(color)

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam.")
        return

    print(" Make sure the scene is empty, then press 'b' to capture background.")
    print(" Color options: 'r' for red, 'g' for green, 'b' for blue, 'y' for yellow, 'k' for black")
    print(" Press 'q' to quit.")

    background = None
    current_color = 'red'  # default color

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        if background is None:
            cv2.putText(frame, "Press 'b' to capture background", (20, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow("Color Invisibility Cloak", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('b'):
                print(" Capturing background...")
                background = get_background(cap)
                print(" Background captured.")
            elif key == ord('q'):
                break
            continue

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        bounds = get_color_bounds(current_color)

        if current_color == 'red':
            # Special case for red (wraps around hue value)
            mask1 = cv2.inRange(hsv, np.array(bounds[0]), np.array(bounds[1]))
            mask2 = cv2.inRange(hsv, np.array(bounds[2]), np.array(bounds[3]))
            color_mask = cv2.bitwise_or(mask1, mask2)
        else:
            color_mask = cv2.inRange(hsv, np.array(bounds[0]), np.array(bounds[1]))

        # Clean the mask
        color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN,
                                    np.ones((3, 3), np.uint8), iterations=2)
        color_mask = cv2.dilate(color_mask, np.ones((3, 3), np.uint8), iterations=1)
        color_mask = cv2.GaussianBlur(color_mask, (5, 5), 0)

        inverse_mask = cv2.bitwise_not(color_mask)
        current_no_cloak = cv2.bitwise_and(frame, frame, mask=inverse_mask)
        cloak_area_from_bg = cv2.bitwise_and(background, background, mask=color_mask)
        final = cv2.addWeighted(current_no_cloak, 1, cloak_area_from_bg, 1, 0)

        # Display current color and instructions
        cv2.putText(final, f"Current color: {current_color}", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2, cv2.LINE_AA)
        cv2.putText(final, "Press 'r/g/b/y/k' to change color | 'b' to recapture bg | 'q' to quit",
                    (15, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2, cv2.LINE_AA)

        cv2.imshow("Color Invisibility Cloak", final)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('b'):
            print(" Re-capturing background...")
            background = get_background(cap)
            print(" Background updated.")
        elif key == ord('r'):
            current_color = 'red'
            print(" Switched to red")
        elif key == ord('g'):
            current_color = 'green'
            print(" Switched to green")
        elif key == ord('b'):
            current_color = 'blue'
            print(" Switched to blue")
        elif key == ord('y'):
            current_color = 'yellow'
            print(" Switched to yellow")
        elif key == ord('k'):
            current_color = 'black'
            print(" Switched to black")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()