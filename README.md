# CS419-Project

## Prerequisites

To host the server locally, please install the requirements:

- Python 3 environment

Please install the requirements manually
```cmd
pip install fastapi
pip install "uvicorn[standard]"
pip install torch
pip install torchvision
pip install opencv-python
pip install tqdm
pip install pandas
pip install efficientnet_pytorch
pip install numpy
```
or you may install from requirements.txt

```cmd
pip install -r requirements.txt
```

## Host the back-end server locally

If you use model 4 (sift + kNN), please download the vector file [here](https://drive.google.com/file/d/1nliTr71AyFzF97-WMNIm-aGQy-7PlA1A/view?usp=sharing) then place `model4_vec.pickle` to `process/collection_vector`.

If you use model 6, 7, or 8 (which is the default model), please go [here](https://drive.google.com/drive/folders/1ih3FqVe7qBcq0diyYZyXu96KHmslTMyN) and:
+ Download the file `efficientb0_right.zip`, copy them to `...\CS419-Project\process\misc\model3\weight` and extract it.
+ Download the file `resnet18_noval.zip`, copy them to `...\CS419-Project\process\misc\model3\weight` and extract it.
+ Download the file `resnet50_noval.zip`, copy them to `...\CS419-Project\process\misc\model3\weight` and extract it.
+ Download the file `model_b0_noval_rec.pickle`, copy them to `...\CS419-Project\process\collection_vector`.

After installing all the dependencies, open the terminal and change the directory to our submitted folder "...\CS419-Project" and run:
```cmd
uvicorn --host 127.0.0.1 --port 8000 backend.main:app --reload --reload-include config.ini
```
Please wait until `uvicorn` displays that application startup complete.

## Use the front-end
Please keep the hosted back-end server running for the front-end to work.

After hosting the back-end server locally, go to the link [here](https://project-cs419-feir.netlify.app/) for our front-end server. 

If the above link doesn't work, please be patient and do the following to run the frontend locally:
+ install `nodejs` (so that the command `npm` works in your terminal)
+ change the directory to `...\CS419-Project\feir`
+ run the command `npm install` and *patiently* waits for the command to complete.
+ run the command `npm start` and wait for `localhost:3000` to open in your browser.

**NOTE: ** There are some unknown errors when using the front-end with Firefox Browser. Please use Microsoft Edge, Chromium, or Google Chrome as these are the browsers we tested on. Furthermore, if your browser disables `CORS`, please go to the settings and enable it.

**NOTE 2: Please don't press `Search` button multiple times impatiently, instead, please wait patiently for response from back-end server. Please.**

## Advanced: change the retrieval model in the back-end server

Change the row `model=` in file `config.ini`. The model value, which is an integer, is commented in the `config.ini` file. If you are hosting the back-end server during the change using the above command, it is supposed to be automatically restarted.
