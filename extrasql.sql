-- create odm2extra schema, sequences, and views
CREATE SCHEMA odm2extra
  AUTHORIZATION postgres;


CREATE SEQUENCE odm2extra."Measurementresultvaluefile_valueFileid_seq"
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE odm2extra."Measurementresultvaluefile_valueFileid_seq"
  OWNER TO postgres;


CREATE SEQUENCE odm2extra."featureactionNamesid_seq"
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 664
  CACHE 1;
ALTER TABLE odm2extra."featureactionNamesid_seq"
  OWNER TO postgres;


CREATE SEQUENCE odm2extra.processdataloggerfile_id_seq
  INCREMENT 1
  MINVALUE 0
  MAXVALUE 9223372036854775807
  START 175
  CACHE 1;
ALTER TABLE odm2extra.processdataloggerfile_id_seq
  OWNER TO postgres;


CREATE TABLE odm2extra."Measurementresultvaluefile"
(
  "valueFileid" serial NOT NULL,
  "valueFile" character varying(100) NOT NULL,
  resultid bigint NOT NULL,
  CONSTRAINT "Measurementresultvaluefile_pkey" PRIMARY KEY ("valueFileid"),
  CONSTRAINT "Measurementres_resultid_12190167_fk_measurementresults_resultid" FOREIGN KEY (resultid)
      REFERENCES odm2.measurementresults (resultid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);
ALTER TABLE odm2extra."Measurementresultvaluefile"
  OWNER TO postgres;

CREATE TABLE odm2extra."featureactionsNames"
(
  featureactionid integer NOT NULL,
  name character(500),
  "featureactionNamesid" integer NOT NULL DEFAULT nextval('odm2extra."featureactionNamesid_seq"'::regclass),
  CONSTRAINT "featureactionNamesid" PRIMARY KEY ("featureactionNamesid"),
  CONSTRAINT featureactionid FOREIGN KEY (featureactionid)
      REFERENCES odm2.featureactions (featureactionid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE odm2extra."featureactionsNames"
  OWNER TO postgres;


CREATE TABLE odm2extra.processdataloggerfile
(
  processdataloggerfileid integer NOT NULL DEFAULT nextval('odm2extra.processdataloggerfile_id_seq'::regclass),
  dataloggerfileid integer NOT NULL,
  "processingCode" character varying(255),
  date_processed timestamp with time zone NOT NULL,
  databeginson integer,
  columnheaderson integer,
  CONSTRAINT processdataloggerfile_pkey PRIMARY KEY (processdataloggerfileid),
  CONSTRAINT processdataloggerfile_dataloggerfileid_fkey FOREIGN KEY (dataloggerfileid)
      REFERENCES odm2.dataloggerfiles (dataloggerfileid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE odm2extra.processdataloggerfile
  OWNER TO postgres;


-- Index: odm2extra."Measurementresultvaluefile_7bab5296"

-- DROP INDEX odm2extra."Measurementresultvaluefile_7bab5296";

CREATE INDEX "Measurementresultvaluefile_7bab5296"
  ON odm2extra."Measurementresultvaluefile"
  USING btree
  (resultid);



CREATE OR REPLACE VIEW odm2extra.timeseriesresultvaluesext AS 
 SELECT timeseriesresultvalues.valueid,
    timeseriesresultvalues.datavalue,
    timeseriesresultvalues.valuedatetime,
    timeseriesresultvalues.valuedatetimeutcoffset,
    timeseriesresultvalues.censorcodecv,
    timeseriesresultvalues.qualitycodecv,
    timeseriesresultvalues.timeaggregationinterval,
    timeseriesresultvalues.timeaggregationintervalunitsid,
    samplingfeatures.samplingfeaturename,
    samplingfeatures.samplingfeaturetypecv,
    processinglevels.processinglevelcode,
    variables.variablecode,
    units.unitsabbreviation,
    timeseriesresultvalues.resultid,
    cv_aggregationstatistic.name AS aggregationstatisticname
   FROM odm2.timeseriesresultvalues,
    odm2.timeseriesresults,
    odm2.results,
    odm2.featureactions,
    odm2.samplingfeatures,
    odm2.processinglevels,
    odm2.variables,
    odm2.units,
    odm2.cv_aggregationstatistic
  WHERE timeseriesresultvalues.resultid = timeseriesresults.resultid AND timeseriesresults.resultid = results.resultid AND timeseriesresults.aggregationstatisticcv::text = cv_aggregationstatistic.name::text AND results.featureactionid = featureactions.featureactionid AND results.processinglevelid = processinglevels.processinglevelid AND results.variableid = variables.variableid AND results.unitsid = units.unitsid AND featureactions.samplingfeatureid = samplingfeatures.samplingfeatureid
  ORDER BY timeseriesresultvalues.datavalue DESC;

ALTER TABLE odm2extra.timeseriesresultvaluesext
  OWNER TO postgres;

CREATE OR REPLACE VIEW odm2extra.timeseriesresultvaluesextwannotations AS 
 SELECT timeseriesresultvalues.valueid,
    timeseriesresultvalues.datavalue,
    timeseriesresultvalues.valuedatetime,
    timeseriesresultvalues.valuedatetimeutcoffset,
    timeseriesresultvalues.censorcodecv,
    timeseriesresultvalues.qualitycodecv,
    timeseriesresultvalues.timeaggregationinterval,
    timeseriesresultvalues.timeaggregationintervalunitsid,
    samplingfeatures.samplingfeaturename,
    processinglevels.processinglevelcode,
    variables.variablecode,
    units.unitsabbreviation,
    timeseriesresultvalues.resultid,
    cv_aggregationstatistic.name AS aggregationstatisticname,
    annotations.annotationtext
   FROM odm2.timeseriesresultvalues,
    odm2.timeseriesresults,
    odm2.results,
    odm2.featureactions,
    odm2.samplingfeatures,
    odm2.processinglevels,
    odm2.variables,
    odm2.units,
    odm2.cv_aggregationstatistic,
    odm2.timeseriesresultvalueannotations,
    odm2.annotations
  WHERE timeseriesresultvalues.resultid = timeseriesresults.resultid AND timeseriesresultvalues.valueid = timeseriesresultvalueannotations.valueid AND timeseriesresults.resultid = results.resultid AND timeseriesresults.aggregationstatisticcv::text = cv_aggregationstatistic.name::text AND results.featureactionid = featureactions.featureactionid AND results.processinglevelid = processinglevels.processinglevelid AND results.variableid = variables.variableid AND results.unitsid = units.unitsid AND featureactions.samplingfeatureid = samplingfeatures.samplingfeatureid AND timeseriesresultvalueannotations.annotationid = annotations.annotationid
  ORDER BY timeseriesresultvalues.datavalue DESC;

ALTER TABLE odm2extra.timeseriesresultvaluesextwannotations
  OWNER TO postgres;
