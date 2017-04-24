FROM ubuntu:14.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

LABEL description='Django admin app for Observation Data Model 2 (ODM2)' \
      url='https://github.com/miguelcleon/ODM2-Admin' \
      author='Miguel Leon' \
      author_email='leonmi@sas.upenn.edu' \
      development_status='5 - Production/Stable' \
      environment='Console' \
      intended_audience='Science/Research, Developers, Education' \
      license='MIT License' \
      operating_system='OS Independent' \
      programming_language='Python' \
      topic='Scientific/Engineering, Education'

EXPOSE 8000
EXPOSE 5432

# Setting up Miniconda
RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion \
    nano curl tar

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda2-4.1.11-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

ENV PATH /opt/conda/bin:$PATH

# Setting up postgresql database
RUN apt-get update --fix-missing && apt-get install -y postgresql postgresql-contrib postgis postgresql-9.3-postgis-2.1

RUN git clone "https://github.com/miguelcleon/ODM2-Admin"

RUN service postgresql start && sudo -u postgres createdb odm2_db && \
    sudo -u postgres pg_restore -d odm2_db -1 -v "/ODM2-Admin/ODM2AdminExamplePostgresqlDB" && \
    sudo -u postgres psql -U postgres -d postgres -c "alter user postgres with password 'test';"

# creates an env with the depepencies
RUN conda create --yes -n odm2adminenv python=2.7 --file /ODM2-Admin/requirements.txt

CMD ["/bin/bash"]
