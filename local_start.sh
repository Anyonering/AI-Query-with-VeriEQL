#!/bin/bash

cd /backend
python3 -m uvicorn main:app --host 0.0.0.0 --reload --port 8000

cd /frontend
npm run dev