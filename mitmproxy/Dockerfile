FROM docker.appdirect.tools/appdirect/mitmproxy:2.0.2
MAINTAINER PSDS India <psds-india@appdirect.com>

COPY redirect.py /home/mitmproxy/

#ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["mitmdump", "-s", "/home/mitmproxy/redirect.py"]
