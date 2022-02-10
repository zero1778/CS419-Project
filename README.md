# CS419-Project

Weight of model 4 (sift) can be downloaded at https://drive.google.com/file/d/1nliTr71AyFzF97-WMNIm-aGQy-7PlA1A/view?usp=sharing then place it to `process/collection_vector`


To host the server locally, please install the requirements:

- Python environment
- pip install fastapi
- pip install "uvicorn[standard]"
- pip install torch
- pip install torchvision
- pip install opencv-python
- pip install tqdm
- pip install pandas
- pip install efficientnet_pytorch
- pip install numpy


After install all the dependencies, please open the terminal and change the directory to our submitted folder "...\CS419-Project". 
Then type "uvicorn --host 127.0.0.1 --port 8000 backend.main:app --reload"