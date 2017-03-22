FROM python:3.6.0
EXPOSE 80
RUN cd ~ \
	&& git clone https://github.com/bhorgaurav/django-first.git \
	&& cd django-first \
	&& chmod +x setup.sh \
	&& chmod +x run.sh \
	&& sh setup.sh

CMD cd ~/django-first \
	&& sh ~/django-first/run.sh
