FROM python:onbuild

RUN pip install -e .

EXPOSE 5000

CMD ["python", "AssociationEngine/Examples/webpage/Server.py"]

