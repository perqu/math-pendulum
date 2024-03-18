import cv2
import numpy as np

def fluctuation_counter(video_path: str, target_color: list[int]) -> float:
    """
    Detects the period of color fluctuations in a video.

    This function analyzes a video to detect the period of color fluctuations
    corresponding to the specified target color. It returns the estimated period
    based on the number of detected color changes.

    Parameters:
    - video_path (str): The path to the video file.
    - target_color (list): The RGB color values of the target color.

    Returns:
    - float: The estimated period of color fluctuations.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Cannot open video file.")
        return

    # Convert target color to HSV format
    target_color_hsv = cv2.cvtColor(np.uint8([[target_color]]), cv2.COLOR_BGR2HSV)[0][0]
    counter = 0
    current_time = None
    was_color_detected_before  = False
    is_color_detected  = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert colors from BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Determine the range of the target color in HSV color space
        lower_color = np.array([target_color_hsv[0] - 10, 100, 100])
        upper_color = np.array([target_color_hsv[0] + 10, 255, 255])

        # Create a mask for the target color
        mask = cv2.inRange(hsv, lower_color, upper_color)

        # Check if the target color is present in the frame
        if cv2.countNonZero(mask) > 0:
            is_color_detected  = True
        else:
            is_color_detected  = False

        if was_color_detected_before  == False and is_color_detected  == True:
            counter +=1
            current_time = cap.get(cv2.CAP_PROP_POS_MSEC)/1000
            print("Current period: ", current_time/counter)

        was_color_detected_before  = is_color_detected 

        '''
        display frames
        cv2.imshow('Frame', frame)
        cv2.imshow('Mask', mask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        '''
    cap.release()
    return current_time/counter

def calculate_gravity_acceleration(period: float, length: float) -> float:
    """
    Calculates the gravity acceleration based on the period of a pendulum.

    This function calculates the gravity acceleration using the period of a pendulum
    and its length. It applies the formula: gravity acceleration = (length * 4 * pi^2) / period^2.

    Parameters:
    - period (float): The period of the pendulum's oscillation.
    - length (float): The length of the pendulum.

    Returns:
    - float: The estimated gravity acceleration.
    """
    return length*4*np.pi**2/(period*period)