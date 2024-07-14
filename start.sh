#!/bin/bash

# Navigate to the backend directory and start the Django server
cd mochi_bot_backend
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000 &

# Navigate to the frontend directory and start the React server
cd ../mochi_bot_frontend
echo "Starting React server..."
npm start