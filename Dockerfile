FROM python

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install pymongo && pip install streamlit && pip install assemblyai

EXPOSE 8501

CMD ["streamlit","run","video.py"]
