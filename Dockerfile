FROM python:3.7 as base

FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base
ENV ACCOUNT_NAME="ACCOUNT_NAME"
ENV ACCOUNT_KEY="ACCOUNT_KEY"
COPY --from=builder /install /usr/local
COPY app /app
WORKDIR /app
CMD ["python","app.py"]