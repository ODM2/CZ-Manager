-- Batched SQL script to fix quality codes for empty annotations since 2023-01-01
-- Run this script using psql: psql -f fix_quality_codes_batched.sql

-- Begin transaction
BEGIN;

-- Set a longer statement timeout (4 minutes per batch)
SET statement_timeout = 240000;

-- Define function to process each sampling feature in batches
CREATE OR REPLACE FUNCTION fix_quality_codes_batched(feature_code text, batch_size integer DEFAULT 100)
RETURNS void AS $$
DECLARE
    sf_id integer;
    good_quality_id text;
    fa_ids integer[];
    total_fixed integer := 0;
    total_deleted integer := 0;
    batch_fixed integer;
    batch_deleted integer;
    has_more boolean := true;
    last_processed_id integer := 0;
BEGIN
    -- Get the sampling feature ID
    SELECT samplingfeatureid INTO sf_id
    FROM odm2.samplingfeatures
    WHERE LOWER(samplingfeaturecode) = LOWER(feature_code);

    -- Check if sampling feature exists
    IF sf_id IS NULL THEN
        RAISE NOTICE 'Sampling feature not found: %', feature_code;
        RETURN;
    END IF;

    -- Get the Good quality code
    SELECT name INTO good_quality_id
    FROM odm2.cv_qualitycode
    WHERE name = 'Good';

    -- Get all feature action IDs for this sampling feature
    SELECT array_agg(featureactionid) INTO fa_ids
    FROM odm2.featureactions
    WHERE samplingfeatureid = sf_id;

    -- Check if feature actions exist
    IF fa_ids IS NULL OR array_length(fa_ids, 1) IS NULL THEN
        RAISE NOTICE 'No feature actions found for %', feature_code;
        RETURN;
    END IF;

    -- Process in batches to avoid timeouts
    WHILE has_more LOOP
        -- Step 1: Find next batch of values with empty annotations
        WITH target_annotations AS (
            SELECT
                a.annotationid,
                tsrv.valueid
            FROM odm2.timeseriesresultvalues tsrv
            JOIN odm2.timeseriesresults tsr ON tsrv.resultid = tsr.resultid
            JOIN odm2.results r ON tsr.resultid = r.resultid
            JOIN odm2.timeseriesresultvalueannotations tsrva ON tsrv.valueid = tsrva.valueid
            JOIN odm2.annotations a ON tsrva.annotationid = a.annotationid
            WHERE
                r.featureactionid = ANY(fa_ids)
                AND tsrv.valuedatetime >= '2023-01-01'
                AND tsrv.valueid > last_processed_id
                AND ((a.annotationcode LIKE '%valid%' AND
                     (a.annotationtext LIKE '%valid :%' OR length(a.annotationtext) < 15))
                    OR
                    (a.annotationcode LIKE '%result comment%' AND
                     (a.annotationtext LIKE '%result comment:%' OR length(a.annotationtext) < 25)))
            ORDER BY tsrv.valueid
            LIMIT batch_size
        ),
        -- Delete annotation links
        delete_anno_links AS (
            DELETE FROM odm2.timeseriesresultvalueannotations
            WHERE valueid IN (SELECT valueid FROM target_annotations)
            RETURNING valueid
        ),
        -- Delete annotations
        delete_annotations AS (
            DELETE FROM odm2.annotations
            WHERE annotationid IN (SELECT annotationid FROM target_annotations)
            RETURNING annotationid
        ),
        -- Update quality codes
        update_values AS (
            UPDATE odm2.timeseriesresultvalues
            SET qualitycodecv = good_quality_id
            WHERE valueid IN (SELECT valueid FROM delete_anno_links)
            RETURNING valueid
        ),
        -- Get max processed ID for next batch
        max_id AS (
            SELECT COALESCE(MAX(valueid), 0) as max_valueid
            FROM delete_anno_links
        )
        -- Update last processed ID and check if we have more to process
        SELECT
            count(*),
            count(*),
            max_valueid,
            count(*) < batch_size
        INTO
            batch_fixed,
            batch_deleted,
            last_processed_id,
            has_more
        FROM update_values, max_id;

        -- If we didn't process any records in this batch, we're done
        IF batch_fixed = 0 THEN
            has_more := false;
        END IF;

        -- Update totals
        total_fixed := total_fixed + batch_fixed;
        total_deleted := total_deleted + batch_deleted;

        -- Log batch progress
        IF batch_fixed > 0 THEN
            RAISE NOTICE 'Batch processed for %: % values fixed, last ID: %',
                feature_code, batch_fixed, last_processed_id;

            -- Commit each batch to avoid long-running transactions
            COMMIT;
            BEGIN;
        END IF;
    END LOOP;

    -- Log final results
    RAISE NOTICE 'Processing complete for %: % annotations removed, % values fixed',
        feature_code, total_deleted, total_fixed;
END;
$$ LANGUAGE plpgsql;

-- Process each sampling feature with smaller batch size to avoid timeouts
SELECT fix_quality_codes_batched('GRBCR', 100);
SELECT fix_quality_codes_batched('GRBGB', 100);
SELECT fix_quality_codes_batched('GRBGBE', 100);
SELECT fix_quality_codes_batched('GRBLR', 100);
SELECT fix_quality_codes_batched('GRBOR', 100);
SELECT fix_quality_codes_batched('GRBUPR', 100);
SELECT fix_quality_codes_batched('HHHR', 100);

-- Clean up
DROP FUNCTION fix_quality_codes_batched;

-- Final commit
COMMIT;

-- Reset timeout
SET statement_timeout = DEFAULT;