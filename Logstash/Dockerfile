FROM docker.elastic.co/logstash/logstash:7.11.2
RUN rm -f /usr/share/logstash/pipeline/logstash.conf
ADD config/logstash.conf /usr/share/logstash/pipeline/logstash.conf