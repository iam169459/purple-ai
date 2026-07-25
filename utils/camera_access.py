"""
Camera Access Module - See, recognize faces, and respond with voice
Provides camera control, photo capture, and face recognition
"""
import os
import sys
import time
import json
import threading
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path

class CameraAccess:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.temp_dir = self.base_dir / "temp"
        self.memory_dir = self.base_dir / "memory"
        self.temp_dir.mkdir(exist_ok=True)
        self.memory_dir.mkdir(exist_ok=True)
        
        self.face_db_file = self.memory_dir / "face_database.json"
        self.camera = None
        self.is_open = False
        self.is_streaming = False
        self.stream_thread = None
        self._opencv_available = False
        self._face_cascade = None
        self._face_recognizer = None
        self._known_faces = {}  # name -> face_encodings
        self._face_labels = {}
        self._label_counter = 0
        self._voice_callback = None
        
        self._check_opencv()
        self._load_face_database()
        
    def _check_opencv(self):
        """Check if OpenCV is available"""
        try:
            import cv2
            self._opencv_available = True
            
            # Load face cascade
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            if os.path.exists(cascade_path):
                self._face_cascade = cv2.CascadeClassifier(cascade_path)
            
            # Initialize face recognizer
            self._face_recognizer = cv2.face.LBPHFaceRecognizer_create()
            
            return True
        except ImportError:
            return False
    
    def _load_face_database(self):
        """Load known faces from database"""
        try:
            if self.face_db_file.exists():
                with open(self.face_db_file, 'r') as f:
                    data = json.load(f)
                    self._known_faces = data.get('faces', {})
                    self._label_counter = data.get('label_counter', 0)
                    
                    # Rebuild label mapping
                    self._face_labels = {}
                    for name, info in self._known_faces.items():
                        self._face_labels[info.get('label', -1)] = name
                    
                    # Train recognizer if we have faces
                    if self._known_faces:
                        self._train_recognizer()
        except Exception as e:
            print(f"Error loading face database: {e}")
    
    def _save_face_database(self):
        """Save known faces to database"""
        try:
            data = {
                'faces': self._known_faces,
                'label_counter': self._label_counter,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.face_db_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving face database: {e}")
    
    def _train_recognizer(self):
        """Train the face recognizer with known faces"""
        if not self._known_faces or not self._face_recognizer:
            return
        
        try:
            import cv2
            
            faces = []
            labels = []
            
            for name, info in self._known_faces.items():
                label = info.get('label', -1)
                if label == -1:
                    continue
                
                # Load face images
                face_images = info.get('images', [])
                for img_path in face_images:
                    if os.path.exists(img_path):
                        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                        if img is not None:
                            # Detect face in the image
                            detected_faces = self._face_cascade.detectMultiScale(
                                img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
                            )
                            if len(detected_faces) > 0:
                                x, y, w, h = detected_faces[0]
                                face_img = img[y:y+h, x:x+w]
                                face_img = cv2.resize(face_img, (100, 100))
                                faces.append(face_img)
                                labels.append(label)
            
            if faces and labels:
                self._face_recognizer.train(faces, np.array(labels))
                print(f"Trained recognizer with {len(faces)} face(s)")
        except Exception as e:
            print(f"Error training recognizer: {e}")
    
    def set_voice_callback(self, callback):
        """Set callback function for voice responses"""
        self._voice_callback = callback
    
    def _speak(self, text: str):
        """Speak text using callback"""
        if self._voice_callback:
            self._voice_callback(text)
        print(f"[Camera]: {text}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get camera status"""
        return {
            'available': self._opencv_available,
            'is_open': self.is_open,
            'is_streaming': self.is_streaming,
            'known_faces': list(self._known_faces.keys()),
            'face_count': len(self._known_faces)
        }
    
    def open_camera(self, camera_index: int = 0) -> Dict[str, Any]:
        """Open camera"""
        if not self._opencv_available:
            return {
                'success': False,
                'message': 'OpenCV not installed. Run: pip install opencv-python'
            }
        
        if self.is_open:
            return {
                'success': True,
                'message': 'Camera is already open'
            }
        
        try:
            import cv2
            self.camera = cv2.VideoCapture(camera_index)
            
            if not self.camera.isOpened():
                return {
                    'success': False,
                    'message': 'Could not open camera. Check permissions or camera connection.'
                }
            
            self.is_open = True
            
            width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = self.camera.get(cv2.CAP_PROP_FPS)
            
            return {
                'success': True,
                'message': f'Camera opened successfully',
                'resolution': f'{width}x{height}',
                'fps': fps
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error opening camera: {str(e)}'
            }
    
    def close_camera(self) -> Dict[str, Any]:
        """Close camera"""
        if not self.is_open:
            return {
                'success': True,
                'message': 'Camera is not open'
            }
        
        try:
            self.stop_stream()
            
            if self.camera:
                self.camera.release()
                self.camera = None
            
            self.is_open = False
            
            return {
                'success': True,
                'message': 'Camera closed'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error closing camera: {str(e)}'
            }
    
    def take_photo(self, filename: Optional[str] = None) -> Dict[str, Any]:
        """Take a photo from camera"""
        if not self._opencv_available:
            return {'success': False, 'message': 'OpenCV not installed'}
        
        camera_was_open = self.is_open
        if not camera_was_open:
            result = self.open_camera()
            if not result['success']:
                return result
        
        try:
            import cv2
            
            ret, frame = self.camera.read()
            
            if not ret:
                return {'success': False, 'message': 'Could not capture frame from camera'}
            
            if not filename:
                filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            
            filepath = str(self.temp_dir / filename)
            cv2.imwrite(filepath, frame)
            
            analysis = self._analyze_frame(frame)
            
            if not camera_was_open:
                self.close_camera()
            
            file_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
            
            return {
                'success': True,
                'message': 'Photo captured',
                'filepath': filepath,
                'filename': filename,
                'size_kb': round(file_size / 1024, 2),
                'analysis': analysis
            }
            
        except Exception as e:
            if not camera_was_open:
                self.close_camera()
            return {'success': False, 'message': f'Error taking photo: {str(e)}'}
    
    def _analyze_frame(self, frame) -> Dict[str, Any]:
        """Analyze a camera frame for faces"""
        analysis = {
            'has_faces': False,
            'face_count': 0,
            'faces': [],
            'recognized_faces': [],
            'brightness': 0,
            'description': ''
        }
        
        try:
            import cv2
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            analysis['brightness'] = int(cv2.mean(gray)[0])
            
            if self._face_cascade:
                faces = self._face_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
                )
                
                analysis['face_count'] = len(faces)
                analysis['has_faces'] = len(faces) > 0
                
                for (x, y, w, h) in faces:
                    face_info = {
                        'x': int(x), 'y': int(y),
                        'width': int(w), 'height': int(h),
                        'recognized_name': None
                    }
                    
                    # Try to recognize the face
                    if self._face_recognizer and self._known_faces:
                        face_img = gray[y:y+h, x:x+w]
                        face_img = cv2.resize(face_img, (100, 100))
                        
                        try:
                            label, confidence = self._face_recognizer.predict(face_img)
                            if confidence < 70:  # Lower = more confident
                                name = self._face_labels.get(label, "Unknown")
                                face_info['recognized_name'] = name
                                analysis['recognized_faces'].append({
                                    'name': name,
                                    'confidence': round(100 - confidence, 1)
                                })
                        except Exception:
                            pass
                    
                    analysis['faces'].append(face_info)
            
            # Generate description
            if analysis['recognized_faces']:
                names = [f['name'] for f in analysis['recognized_faces']]
                if len(names) == 1:
                    analysis['description'] = f"I can see {names[0]}"
                else:
                    analysis['description'] = f"I can see {', '.join(names)}"
            elif analysis['has_faces']:
                count = analysis['face_count']
                analysis['description'] = f"I can see {count} unknown person(s)"
            else:
                analysis['description'] = "No one is in the camera view"
                
        except Exception as e:
            analysis['description'] = 'Analysis unavailable'
        
        return analysis
    
    def learn_face(self, name: str) -> Dict[str, Any]:
        """Learn and store a face with a name"""
        if not self._opencv_available:
            return {'success': False, 'message': 'OpenCV not installed'}
        
        if not self.is_open:
            result = self.open_camera()
            if not result['success']:
                return result
        
        try:
            import cv2
            
            # Take multiple photos for better recognition
            face_samples = []
            required_samples = 10
            
            self._speak(f"Learning your face, {name}. Look at the camera...")
            
            for i in range(required_samples):
                ret, frame = self.camera.read()
                if not ret:
                    continue
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self._face_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
                )
                
                if len(faces) > 0:
                    x, y, w, h = faces[0]
                    face_img = gray[y:y+h, x:x+w]
                    face_img = cv2.resize(face_img, (100, 100))
                    face_samples.append(face_img)
                
                time.sleep(0.3)
            
            if len(face_samples) < 5:
                return {
                    'success': False,
                    'message': 'Could not capture enough face samples. Make sure your face is visible.'
                }
            
            # Save face images
            face_dir = self.temp_dir / "faces"
            face_dir.mkdir(exist_ok=True)
            
            saved_images = []
            for i, face_img in enumerate(face_samples):
                img_path = str(face_dir / f"{name}_{i}.jpg")
                cv2.imwrite(img_path, face_img)
                saved_images.append(img_path)
            
            # Create or update face entry
            if name not in self._known_faces:
                self._label_counter += 1
                self._known_faces[name] = {
                    'label': self._label_counter,
                    'images': saved_images,
                    'created': datetime.now().isoformat()
                }
            else:
                self._known_faces[name]['images'].extend(saved_images)
                self._known_faces[name]['updated'] = datetime.now().isoformat()
            
            # Update label mapping
            self._face_labels[self._label_counter] = name
            
            # Save database and retrain
            self._save_face_database()
            self._train_recognizer()
            
            return {
                'success': True,
                'message': f"I've learned your face, {name}! I'll remember you.",
                'samples_captured': len(face_samples)
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error learning face: {str(e)}'}
    
    def forget_face(self, name: str) -> Dict[str, Any]:
        """Remove a known face"""
        if name in self._known_faces:
            # Delete saved images
            face_info = self._known_faces[name]
            for img_path in face_info.get('images', []):
                if os.path.exists(img_path):
                    os.remove(img_path)
            
            # Remove from database
            label = face_info.get('label', -1)
            del self._known_faces[name]
            if label in self._face_labels:
                del self._face_labels[label]
            
            self._save_face_database()
            self._train_recognizer()
            
            return {'success': True, 'message': f"I've forgotten {name}"}
        
        return {'success': False, 'message': f"I don't know anyone named {name}"}
    
    def look_at_me(self) -> Dict[str, Any]:
        """Quick camera check - recognize faces and speak"""
        result = self.take_photo()
        
        if not result['success']:
            return result
        
        analysis = result.get('analysis', {})
        
        if analysis.get('recognized_faces'):
            names = [f['name'] for f in analysis['recognized_faces']]
            if len(names) == 1:
                description = f"Hi {names[0]}! I recognize you!"
            else:
                description = f"I see {', '.join(names)}!"
        elif analysis.get('has_faces'):
            count = analysis['face_count']
            if count == 1:
                description = "I can see you, but I don't recognize you yet. Say 'learn my face' to teach me!"
            else:
                description = f"I can see {count} people, but I don't know them yet."
        else:
            description = "No one is in the camera view right now."
        
        return {
            'success': True,
            'message': description,
            'filepath': result['filepath'],
            'analysis': analysis
        }
    
    def recognize_faces(self) -> Dict[str, Any]:
        """Recognize faces in current camera view"""
        if not self._opencv_available:
            return {'success': False, 'message': 'OpenCV not installed'}
        
        if not self.is_open:
            result = self.open_camera()
            if not result['success']:
                return result
        
        try:
            import cv2
            
            ret, frame = self.camera.read()
            if not ret:
                return {'success': False, 'message': 'Could not read from camera'}
            
            analysis = self._analyze_frame(frame)
            
            # Build response message
            if analysis['recognized_faces']:
                names = [f['name'] for f in analysis['recognized_faces']]
                message = f"I see: {', '.join(names)}"
            elif analysis['has_faces']:
                message = f"I see {analysis['face_count']} unknown person(s)"
            else:
                message = "No one is in the camera view"
            
            return {
                'success': True,
                'face_count': analysis['face_count'],
                'recognized_faces': analysis['recognized_faces'],
                'message': message
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error recognizing faces: {str(e)}'}
    
    def start_recognition_stream(self) -> Dict[str, Any]:
        """Start continuous face recognition with voice announcements"""
        if self.is_streaming:
            return {'success': True, 'message': 'Already streaming'}
        
        if not self.is_open:
            result = self.open_camera()
            if not result['success']:
                return result
        
        self.is_streaming = True
        self._last_announced = {}
        self._announcement_cooldown = 10  # seconds between same face announcements
        
        def recognition_loop():
            import cv2
            while self.is_streaming and self.is_open:
                try:
                    ret, frame = self.camera.read()
                    if not ret:
                        continue
                    
                    analysis = self._analyze_frame(frame)
                    current_time = time.time()
                    
                    # Announce recognized faces
                    for face in analysis.get('recognized_faces', []):
                        name = face['name']
                        last_time = self._last_announced.get(name, 0)
                        
                        if current_time - last_time > self._announcement_cooldown:
                            self._speak(f"Hello {name}!")
                            self._last_announced[name] = current_time
                    
                    # Announce unknown faces (with cooldown)
                    if analysis.get('has_faces') and not analysis.get('recognized_faces'):
                        last_unknown = self._last_announced.get('unknown', 0)
                        if current_time - last_unknown > 30:
                            count = analysis['face_count']
                            if count == 1:
                                self._speak("I see someone new! Say 'learn my face' to introduce yourself.")
                            else:
                                self._speak(f"I see {count} new people!")
                            self._last_announced['unknown'] = current_time
                    
                except Exception as e:
                    pass
                
                time.sleep(1)
        
        self.stream_thread = threading.Thread(target=recognition_loop, daemon=True)
        self.stream_thread.start()
        
        return {'success': True, 'message': 'Face recognition started. I\'ll greet known faces!'}
    
    def stop_stream(self) -> Dict[str, Any]:
        """Stop camera stream"""
        self.is_streaming = False
        return {'success': True, 'message': 'Camera stream stopped'}
    
    def get_known_faces(self) -> Dict[str, Any]:
        """Get list of known faces"""
        faces = []
        for name, info in self._known_faces.items():
            faces.append({
                'name': name,
                'label': info.get('label'),
                'image_count': len(info.get('images', [])),
                'created': info.get('created')
            })
        
        return {
            'success': True,
            'faces': faces,
            'count': len(faces)
        }
    
    def get_camera_info(self) -> Dict[str, Any]:
        """Get camera information"""
        if not self._opencv_available:
            return {'available': False, 'message': 'OpenCV not installed'}
        
        try:
            import cv2
            
            info = {'available': True, 'cameras': []}
            
            for i in range(10):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    
                    info['cameras'].append({
                        'index': i,
                        'resolution': f'{width}x{height}',
                        'fps': fps
                    })
                    cap.release()
            
            return info
            
        except Exception as e:
            return {'available': False, 'message': f'Error: {str(e)}'}
    
    # Always-on Object Recognition
    def start_object_recognition(self) -> Dict[str, Any]:
        """Start always-on object recognition - camera always watching"""
        if self.is_streaming:
            return {'success': True, 'message': 'Already streaming'}
        
        if not self.is_open:
            result = self.open_camera()
            if not result['success']:
                return result
        
        self.is_streaming = True
        self._last_object_announce = {}
        self._object_cooldown = 15  # seconds between same object announcements
        self._voice_callback = None
        
        def object_recognition_loop():
            import cv2
            last_faces = []
            
            while self.is_streaming and self.is_open:
                try:
                    ret, frame = self.camera.read()
                    if not ret:
                        continue
                    
                    analysis = self._analyze_frame(frame)
                    current_time = time.time()
                    
                    # Check for new faces
                    current_faces = [f.get('recognized_name') for f in analysis.get('recognized_faces', []) if f.get('recognized_name')]
                    
                    # Announce new faces
                    for name in current_faces:
                        if name not in last_faces:
                            last_time = self._last_object_announce.get(f'face_{name}', 0)
                            if current_time - last_time > self._object_cooldown:
                                if self._voice_callback:
                                    self._voice_callback(f"Hello {name}!")
                                self._last_object_announce[f'face_{name}'] = current_time
                    
                    # Announce unknown faces
                    unknown_count = analysis.get('face_count', 0) - len(current_faces)
                    if unknown_count > 0:
                        last_time = self._last_object_announce.get('unknown_face', 0)
                        if current_time - last_time > 30:
                            if self._voice_callback:
                                self._voice_callback(f"I see {unknown_count} new {'person' if unknown_count == 1 else 'people'}")
                            self._last_object_announce['unknown_face'] = current_time
                    
                    last_faces = current_faces
                    
                    # Detect motion or significant changes
                    # (basic brightness/movement detection)
                    
                except Exception as e:
                    pass
                
                time.sleep(1)
        
        self.stream_thread = threading.Thread(target=object_recognition_loop, daemon=True)
        self.stream_thread.start()
        
        return {'success': True, 'message': 'Camera always watching! I\'ll recognize faces and objects.'}
    
    def what_do_i_show(self) -> Dict[str, Any]:
        """Analyze what user is showing to camera"""
        if not self.is_open:
            result = self.open_camera()
            if not result['success']:
                return result
        
        try:
            import cv2
            
            ret, frame = self.camera.read()
            if not ret:
                return {'success': False, 'message': 'Could not read from camera'}
            
            analysis = self._analyze_frame(frame)
            
            # Build detailed response
            response = {
                'success': True,
                'faces': analysis.get('recognized_faces', []),
                'face_count': analysis.get('face_count', 0),
                'brightness': analysis.get('brightness', 0),
                'description': ''
            }
            
            if analysis.get('recognized_faces'):
                names = [f['name'] for f in analysis['recognized_faces']]
                response['description'] = f"I can see {', '.join(names)}"
            elif analysis.get('has_faces'):
                response['description'] = f"I can see {analysis['face_count']} {'person' if analysis['face_count'] == 1 else 'people'}"
            else:
                response['description'] = "I can see the camera view"
            
            return response
            
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def describe_scene(self) -> str:
        """Get a natural description of what's in view"""
        result = self.what_do_i_show()
        if result['success']:
            return result['description']
        return "I can't see anything right now"


# Create global instance
camera_access = CameraAccess()