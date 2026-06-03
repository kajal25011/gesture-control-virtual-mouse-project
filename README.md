# Gesture Control Virtual Mouse

A Gesture Control Virtual Mouse is a computer vision-based application that allows users to control the mouse cursor using hand gestures instead of a physical mouse. The system captures real-time video through a webcam, detects hand landmarks, and performs mouse operations such as cursor movement, clicking, and scrolling.

## Features

- Real-time hand tracking using webcam
- Mouse cursor movement through finger gestures
- Left click functionality
- Right click functionality
- Scroll control using hand gestures
- User-friendly web interface
- Fast and accurate gesture recognition

## Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Libraries
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

## System Architecture

- Frontend developed using HTML, CSS, and JavaScript.
- Backend developed using Python and Flask.
- Flask acts as a bridge between the frontend and backend.
- OpenCV captures webcam input.
- MediaPipe detects hand landmarks.
- PyAutoGUI performs mouse actions based on detected gestures.

## Project Workflow

1. User opens the web application.
2. Flask server starts the backend services.
3. Webcam captures live video feed.
4. MediaPipe detects hand landmarks.
5. Hand gestures are analyzed.
6. Corresponding mouse actions are triggered.
7. Cursor movement and clicks are executed on the system.

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/gesture-control-virtual-mouse.git
cd gesture-control-virtual-mouse
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

### Open Browser

```text
 http://127.0.0.1:5000
```
## Note

This project is currently configured to run locally using Flask.

After starting the Flask server with:

python app.py

Open your browser and visit:

http://127.0.0.1:5000
## Project Structure

```text
Gesture-Control-Virtual-Mouse/
│
├── static/
│   ├── css/
│   ├── js/
│
├── templates/
│   └── index.html
│
├── app.py
├── gesture_controller.py
├── requirements.txt
└── README.md
```

## Future Enhancements

- Drag and drop functionality
- Multi-hand gesture support
- Custom gesture mapping
- Voice command integration
- Improved gesture accuracy using AI models

## Author

Kajal Wavare

## License

This project is developed for educational and learning purposes.
