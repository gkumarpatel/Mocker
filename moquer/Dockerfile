FROM docker.appdirectondemand.com/appdirect/tomcat:1.0.59
MAINTAINER PSDS India <psds-india@appdirect.com>

ENV JAVA_OPTS -Xms384m -Xmx384m -XX:MaxMetaspaceSize=64m

ENV CATALINA_OPTS="-DendPoint=dockerdevmoquer.appdirect.com"

COPY moquer.war $CATALINA_HOME/webapps/ROOT.war
