# Smart Farming Assistant - Viva One Sheet

## 1) Project Title
Smart Farming Assistant (Real-Time Pest and Disease Alert System)

## 2) Problem Statement
Farmers often face crop disease and pest issues without quick expert guidance. This project provides early reporting, disease prediction from images, and practical recommendations through a simple web interface.

## 3) Objective
- Let users submit crop problem reports with image and location.
- Predict plant disease from uploaded leaf images.
- Provide guidance and chat support.
- Give admin dashboard for user/report management.

## 4) System Architecture
- Frontend: Static web pages (HTML, CSS, JavaScript).
- Backend: Node.js + Express server.
- ML Service: Python Flask API with TensorFlow model.
- Database: MongoDB (via Mongoose).
- Communication: Backend calls Python API over HTTP.

## 5) Technologies Used
### Frontend
- HTML5
- CSS3
- Vanilla JavaScript

### Backend (Node.js)
- Express
- body-parser
- cors
- dotenv
- axios
- form-data
- multer (image upload)
- jsonwebtoken (auth)
- bcryptjs (password hashing)
- mongoose (MongoDB)
- nodemailer (email alerts)
- selfsigned (optional HTTPS dev certificates)

### Python ML API
- Flask
- TensorFlow / Keras
- NumPy
- Pillow
- h5py

### Database
- MongoDB

## 6) Core Features Implemented
- User signup/login with JWT authentication.
- Crop report submission with optional image upload.
- Disease prediction endpoint integration (`/predict`, `/predict-fruit`).
- Admin panel for viewing/updating/deleting reports and users.
- Chat endpoint for farmer assistance.
- Translation endpoint (English/Hindi support path).
- Weather geocode support.
- Email notification to admin on new reports.

## 7) APIs / External Services Used
- Python Flask Prediction API (local): `http://127.0.0.1:5000`
- Hugging Face Router API (chat model routing)
- Groq SDK path (when key/package available) with fallback behavior
- MyMemory Translation API
- OpenWeather Geocoding API
- Gmail SMTP (via nodemailer)

## 8) Model and AI Components
- Leaf disease model file loaded from: `python_api/models/leaf_model.keras`
- Inference done in Python API and consumed by Node backend.
- Confidence-based response handling in backend.
- If AI keys are unavailable, backend uses fallback guidance for stability.

## 9) Security and Validation
- JWT-based auth routes.
- Password hashing using bcryptjs.
- Input validation and request size limits.
- Multer upload size limit (10 MB).
- Environment variable based secret/config handling.

## 10) Run-Time Ports
- Node backend: `http://localhost:3000`
- Python API: `http://127.0.0.1:5000`

## 11) Folder Highlights
- `frontend/` -> UI pages
- `backend/` -> Node API, auth, routes, DB config
- `python_api/` -> Flask app + ML model files
- `backend/uploads/reports/` -> Uploaded report images

## 12) What to Say in Viva (Short Pitch)
This is a full-stack smart agriculture assistant. The frontend collects farmer issues, the Node backend handles authentication, reports, and admin workflows, and a separate Python TensorFlow service predicts crop disease from images. The system also supports chat guidance, translation, weather lookup, and email alerts, making it practical for real-time field use.
