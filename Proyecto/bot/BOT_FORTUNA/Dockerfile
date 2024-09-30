FROM chatscript-base:latest as base
# Si se definen en docker-compose.yml no funcionan las variables en Dockerfile

FROM base AS bot_fortuna

ENV BOTNAME BOT_FORTUNA
ENV PORT 10601

WORKDIR /opt/alloxentric/
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
#COPIA LA CARPETA DEL BOT A RAWDATA
COPY ${BOTNAME}/BOT ChatScript/RAWDATA/${BOTNAME}
#COPIA LOS ARCHIVOS A RAWDATA
COPY filesBOTNAME.txt ChatScript/RAWDATA/files${BOTNAME}.txt
#DEFINE LAS RUTAS EN EL ARCHIVO DEL BOT
RUN sed -i s/BOTNAME/${BOTNAME}/g ChatScript/RAWDATA/files${BOTNAME}.txt
#COPY bots_healtcheck.sh /bots_healthcheck.sh
#RUN chmod +x /bots_healthcheck.sh
WORKDIR /opt/alloxentric/ChatScript
COPY healthcheck.pl .
USER root
ENTRYPOINT ["/docker-entrypoint.sh"]
#CMD tail -f /dev/null
