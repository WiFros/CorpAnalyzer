FROM nvcr.io/nvidia/pytorch:24.01-py3

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
 
COPY ./ /code
 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]