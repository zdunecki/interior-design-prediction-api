FROM python:3.6

# args
ARG KAGGLE_USER_NAME
ARG KAGGLE_KEY

WORKDIR /usr/src/app

RUN echo $KAGGLE_USER_NAME

# kaggle config
RUN pip install kaggle
RUN mkdir -p ~/.kaggle
RUN echo "{\"username\": \"${KAGGLE_USER_NAME}\", \"key\": \"${KAGGLE_KEY}\"}" >  ~/.kaggle/kaggle.json
RUN chmod 600 ~/.kaggle/kaggle.json

# get prediciton model from kaggle
RUN kaggle datasets download \
 patrykzdunowski/getartist-models \
 -f interior_styles.h5
RUN unzip interior_styles.h5.zip
RUN mkdir -p data && mv interior_styles.h5 ./data/model.h5

# clear kaggl config
RUN rm -rf ~/.kaggle

# setup python
COPY predict_interior_styles.py ./
COPY requirements.txt ./
RUN pip install -r requirements.txt

CMD [ "python", "predict_interior_styles.py" ]

