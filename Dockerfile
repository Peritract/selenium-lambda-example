FROM public.ecr.aws/lambda/python:3.10
WORKDIR ${LAMBDA_TASK_ROOT}
RUN yum update -y \
    && yum clean all \
    && yum install -y tar gzip bzip2
RUN yum install xz atk cups-libs gtk3 libXcomposite alsa-lib tar \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel unzip bzip2 -y -q
COPY install-firefox.sh .
RUN bash install-firefox.sh
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt
COPY app.py .
CMD [ "app.handler" ]