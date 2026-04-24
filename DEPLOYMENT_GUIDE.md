# Deployment Guide (Node.js + Python Model)

This project has 2 services in production:

1. Node.js backend (serves frontend pages and API)
2. Python Flask model API (leaf/fruit prediction)

## Recommended Hosting

- Backend: Render Web Service (Node)
- Model API: Render Web Service (Python)
- Database: MongoDB Atlas

## Fastest Deploy (Blueprint)

This repo now includes `render.yaml` at project root.

Steps:

1. Push latest code to GitHub.
2. In Render, click **New +** -> **Blueprint**.
3. Connect your GitHub repo and select branch.
4. Render will detect `render.yaml` and create two services automatically:
	- `farmalert-model-api`
	- `farmalert-backend`
5. Fill all `sync: false` environment variables in Render dashboard.

## 1) Prepare MongoDB Atlas

- Create a free cluster on MongoDB Atlas.
- Create a database user.
- Add network access rule `0.0.0.0/0` (or restrict to Render IPs if available).
- Copy connection string as `MONGODB_URI`.

## 2) Deploy Python Model API (Render)

Create new Web Service from this repo:

- Root Directory: `python_api`
- Runtime: Python 3.11+
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

Environment variables:

- `PYTHONUNBUFFERED=1`

Important model files:

- Must exist: `python_api/models/leaf_model.keras` (or supported leaf model file)
- Optional for fruit endpoint: `python_api/models/fruit_model.h5`
- Optional for fruit classes: `python_api/models/fruit_class_names.json`

Health check:

- `GET /health` should return `{ "status": "ok" }`

Copy Python service URL, for example:

- `https://farmalert-model.onrender.com`

## 3) Deploy Node Backend (Render)

Create another Web Service from this repo:

- Root Directory: project root
- Runtime: Node
- Build Command: `npm install`
- Start Command: `npm start`

Set environment variables:

- `NODE_ENV=production`
- `HOST=0.0.0.0`
- `PORT=10000` (or Render default)
- `MONGODB_URI=<your atlas connection string>`
- `JWT_SECRET=<strong-random-secret>`
- `EMAIL_USER=<gmail address>`
- `EMAIL_PASSWORD=<gmail app password>`
- `ADMIN_EMAIL=<admin email>`
- `APP_BASE_URL=<your backend url>`
- `LEAF_PREDICT_API_URL=<python-service-url>/predict`
- `FRUIT_PREDICT_API_URL=<python-service-url>/predict-fruit`

Optional variables:

- `WEATHER_API_KEY=<openweathermap key>`
- `HUGGING_FACE_API_KEY=<hugging-face token>`
- `HUGGING_FACE_MODEL=openai/gpt-oss-120b:fastest`
- `HUGGING_FACE_ROUTER=https://router.huggingface.co/v1/chat/completions`
- `PYTHON_ANALYSIS_TIMEOUT=120000`

## 4) Verify Deployment

Open backend URL:

- Home page should load (frontend is served by backend).
- Test login/signup.
- Test leaf disease upload endpoint from UI.
- Test weather page if API key is set.
- Test chat if Hugging Face key is set.

## 5) Important Notes

- If `fruit_model.h5` is missing, `/predict-fruit` will return 503 in production.
- Email links now use `APP_BASE_URL` (set this to your deployed backend URL).
- Localhost URLs should not be used in production environment variables.

## 6) Quick Rollback Strategy

If prediction fails after deploy:

1. Check Python service logs first.
2. Confirm model files exist in `python_api/models`.
3. Confirm backend env URLs point to the live Python API.
4. Re-deploy backend after env update.
