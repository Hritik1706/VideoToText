#############################################################   STAGE 1   ############################################################################
FROM python:3.9 as backend-builder

WORKDIR /app

COPY . .

RUN  pip install streamlit  &&  pip install pymongo  &&  pip install ffmpeg  &&  pip install git+https://github.com/openai/whisper.git


#############################################################   STAGE 2   ############################################################################

FROM python:3.9-slim

WORKDIR /app

COPY --from=backend-builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/

COPY --from=backend-builder /app /app

EXPOSE 8501

CMD ["/usr/local/bin/streamlit", "run", "video.py"]
