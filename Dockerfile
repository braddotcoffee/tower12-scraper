FROM selenium/standalone-chrome

ADD requirements.txt /
ADD bot.py /
ADD lib /lib

USER root
RUN apt-get update
RUN apt-get install -y python3-distutils
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "python3", "bot.py" ]