FROM dockerfile/python

MAINTAINER <stephane.rault@radicalspam.org>

ENV FACEBOOK_KEY ''
ENV FACEBOOK_SECRET ''

ENV TWITTER_KEY ''
ENV TWITTER_SECRET ''

ENV GOOGLE_KEY ''
ENV GOOGLE_SECRET ''

ENV GITHUB_KEY ''
ENV GITHUB_SECRET ''

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get dist-upgrade -y --no-install-recommends

RUN curl -k -O https://bootstrap.pypa.io/get-pip.py && python get-pip.py && rm -f get-pip.py

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN git clone https://github.com/srault95/flask-social-blueprint.git -b mongodb /data/flask-social-blueprint

WORKDIR /data/flask-social-blueprint/example/mongodb

RUN pip install -r requirements.txt

RUN pip freeze

CMD ["python", "main.py"]

EXPOSE 5055
