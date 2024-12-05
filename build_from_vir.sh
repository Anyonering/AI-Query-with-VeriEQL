#!/bin/bash
# first create a virtual environment
python -m venv venv
source /venv/bin/activate
git clone --recursive https://github.com/Anyonering/AI-Query-with-VeriEQL.git
cd AI-Query-with-VeriEQL
git checkout only-backend
cd backend/
pip install -r requirements.txt
cd verieql
cp -fr z3py_libs/*.py ../../../venv/lib/python3.11/site-packages/z3
chmod -R 777 ../../backend

# run the following command in backend/ to start the server
# python3 -m uvicorn main:app --host 0.0.0.0 --reload --port 8000

