FROM python:3.6

# args
ARG KAGGLE_USER_NAME
ARG KAGGLE_KEY

WORKDIR /usr/src/app

# kaggle config
RUN pip install kaggle
RUN KAGGLE_JSON='{"username":"%s","key":"%s"}\n'
RUN mkdir -p .kaggle
RUN printf "$KAGGLE_JSON" "$KAGGLE_USER_NAME" "$KAGGLE_KEY" > ~/.kaggle/kaggle.json
RUN chmod 600 ~/.kaggle/kaggle.json

# get prediciton model from kaggle
RUN kaggle datasets download \
 patrykzdunowski/getartist-models \
 -f interior_styles.h5
RUN unzip interior_styles.h5.zip
RUN mkdir -p data && mv interior_styles.h5 ./data/model.h5

# setup python
COPY predict_interior_styles.py ./
COPY requirements.txt ./
RUN pip install -r requirequirements.txt

CMD [ "python", "predict.py" ]

