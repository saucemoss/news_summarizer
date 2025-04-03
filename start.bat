@echo off
cd backend
start python api.py
start python scheduler.py 
cd ..
cd frontend
npm start  

