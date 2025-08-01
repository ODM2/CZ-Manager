import os
import csv
import pandas as pd
import re
import logging
from datetime import datetime, timedelta
from multiprocessing import Process
import threading
from functools import wraps  # Add this import for the wraps decorator
import time  # Make sure time is imported at the top level

from django.core.wsgi import get_wsgi_application
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from django.db.utils import OperationalError, DatabaseError

# Initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.developmentPREP")
application = get_wsgi_application()

from odm2admin.models import *
import odm2admin.modelHelpers as modelHelpers

# Configure logging
logging.basicConfig(
    filename='grabdatav2.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)
logger = logging.getLogger(__name__)

# Define column names (from example data)
COLUMN_NAMES = [
    'STATION ID', 'STATION ALIAS ID', 'STATION NAME', 'STATION TYPE', 'TOWN', 'COUNTY',
    'STATE', 'LATITUDE DECIMAL DEGREE', 'LONGITUDE DECIMAL DEGREE', 'LOCATION METHOD',
    'MAP SCALE', 'LOCATION DATUM', 'WATERBODY ID', 'WATERBODY NAME', 'RIVER NAME',
    'DESIGNATED RIVER NAME', 'RELATED LAKE NAME', 'HUC 12 CODE',
    'STATION ACTIVITY STATUS', 'ACTIVITY ID', 'ACTIVITY TYPE', 'REPLICATE NUMBER REFERENCE',
    'DATA STATUS', 'MEDIUM', 'DEPTH ZONE', 'DEPTH', 'DEPTH UNITS', 'UPPER DEPTH',
    'LOWER DEPTH', 'DEPTH RANGE UNITS', 'START DATE', 'START TIME', 'RAIN PRIOR 3 DAYS',
    'SAMPLE COLLECTION METHOD ID', 'ACTIVITY COMMENTS', 'PARAMETER/ANALYTE',
    'QUALIFIER AND RESULTS', 'UNITS', 'RESULT COMMENTS', 'LAB QUALIFIER', 'LAB ID',
    'ANALYTICAL METHOD', 'ANALYTICAL METHOD SOURCE ID', 'RESULT VALID', 'RDL',
    'METHOD DETECTION LIMIT', 'DETECTION LIMIT COMMENTS', 'FRACTION TYPE',
    'STATISTIC TYPE', 'SAMPLE SIZE', 'Date Last Modified',
    'PROJECT: Volunteer Lake Assessment Program; ORGANIZATION: New Hampshire Department Of Environmental Services; PROJECT MANAGER: Sara Steiner (Sara.E.Steiner@Des.Nh.Gov)*'
]

# Define constants for column names
PARAMETER_ANALYTE = 'PARAMETER/ANALYTE'
QUALIFIER_RESULTS = 'QUALIFIER AND RESULTS'
UNITS = 'UNITS'
RESULT_VALID = 'DATA STATUS'
RDL = 'RDL'
START_DATE = 'START DATE'
DETECTION_LIMIT = 'METHOD DETECTION LIMIT'
DETECTION_LIMIT_COMMENTS = 'DETECTION LIMIT COMMENTS'
START_TIME = 'START TIME'
STATION_ID = 'STATION ID'
STATION_NAME = 'STATION NAME'
ACTIVITY_ID = 'ACTIVITY ID'
ACTIVITY_TYPE = 'ACTIVITY TYPE'
ANALYTICAL_METHOD = 'ANALYTICAL METHOD'
ANALYTICAL_METHOD_SOURCE_ID = 'ANALYTICAL METHOD SOURCE ID'
DEPTH_ZONE = 'DEPTH ZONE'
MEDIUM = 'MEDIUM'
LAB_ID = 'LAB ID'
DEPTH = 'DEPTH'
DEPTH_UNITS = 'DEPTH UNITS'
RESULT_COMMENTS = 'RESULT COMMENTS'


# Retry decorator for database operations
def db_retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (IntegrityError, OperationalError, DatabaseError) as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    logger.warning(f"Database operation failed: {e}. Retrying ({attempts}/{max_attempts})...")
                    # Reset connection before retry
                    connection.close()
                    time.sleep(delay)
            return None  # Return None if all attempts fail but don't reach the raise

        return wrapper

    return decorator


# Cache for lookup values
constant_cache = {
    'processinglevels': None,
    'medium': None,
    'resulttype': None,
    'methtype': None,
    'aggstat': None,
    'variable_type_map': {},
    'cvvariablename_map': {}
}


def init_constant_lookups():
    """
    Initialize constant lookups with error handling.
    This prevents having to repeatedly query the database for common values.
    """
    try:
        constant_cache['processinglevels'] = Processinglevels.objects.get(processinglevelid=1)
        constant_cache['medium'] = CvMedium.objects.get(name='Liquid aqueous')
        constant_cache['resulttype'] = CvResulttype.objects.get(name='Time series coverage')
        constant_cache['methtype'] = CvMethodtype.objects.get(name='Specimen analysis')
        constant_cache['aggstat'] = CvAggregationstatistic.objects.get(name='Continuous')
        try:
            constant_cache['methtype'] = CvMethodtype.objects.get(name='Specimen analysis')
            logger.info(f"Retrieved method type: {constant_cache['methtype']}")
        except CvMethodtype.DoesNotExist:
            logger.error("Method type 'Specimen analysis' not found in database")
            return False
        except Exception as e:
            logger.error(f"Error retrieving method type: {e}")
            return False
        # Cache all variable types to avoid repeated lookups - look for both formats of water quality
        for vartype in CvVariabletype.objects.all():
            constant_cache['variable_type_map'][vartype.name.lower()] = vartype
            # Also add without spaces to catch camelCase
            constant_cache['variable_type_map'][vartype.name.lower().replace(' ', '')] = vartype

        # Try to get water quality with different formats
        # This is the code that's failing to find or create the water quality variable type
        water_quality_vartype = None
        for vartype_name in ['Water quality', 'WaterQuality', 'waterquality', 'water quality']:
            try:
                water_quality_vartype = CvVariabletype.objects.get(name='Water quality')
                if water_quality_vartype:
                    logger.info(f"Found 'Water quality' variable type as: {water_quality_vartype}")
                    break
            except Exception as e:
                logger.error(f"Error searching for water quality vartype '{vartype_name}': {e}")

        # If not found, create it - this is failing
        if not water_quality_vartype:
            try:
                water_quality_vartype = CvVariabletype.objects.create(
                    name='Water quality',
                    term='WaterQuality',
                    definition='Variables associated with water quality variables or processes'
                )
                logger.info(f"Created missing 'Water quality' variable type: {water_quality_vartype}")
            except Exception as e:
                logger.error(f"Error creating water quality variable type: {e}")

        # Add to cache with various keys for flexibility
        if water_quality_vartype:
            constant_cache['variable_type_map']['water quality'] = water_quality_vartype
            constant_cache['variable_type_map']['waterquality'] = water_quality_vartype
            constant_cache['default_variable_type'] = water_quality_vartype

        # Pre-cache commonly used CvVariablename entries to avoid repeated lookups
        common_vars = [
            'Coliform, fecal', 'Temperature', 'pH', 'Dissolved oxygen',
            'Salinity', 'Light attenuation coefficient', 'Escherichia Coli'
        ]
        for var_name in common_vars:
            try:
                var_objs = list(CvVariablename.objects.filter(name__iexact=var_name))
                if var_objs:
                    constant_cache['cvvariablename_map'][var_name.lower()] = var_objs[0]
                    logger.info(f"Cached variable name: {var_name} -> {var_objs[0]}")
            except Exception as e:
                logger.error(f"Error caching variable {var_name}: {e}")

        # Handle "TOTAL FECAL COLIFORM" specifically since it appears often in your data
        try:
            # Try to find the equivalent in the database
            total_fecal_coliform = findCVVar("TOTAL FECAL COLIFORM")
            if total_fecal_coliform:
                # Make sure it's in the cache
                constant_cache['cvvariablename_map']["total fecal coliform"] = total_fecal_coliform
                logger.info(f"Cached 'TOTAL FECAL COLIFORM' as {total_fecal_coliform}")
        except Exception as e:
            logger.error(f"Error caching 'TOTAL FECAL COLIFORM': {e}")

        logger.info("Successfully initialized constant lookups")
        return True
    except Exception as e:
        logger.error(f"Error initializing constant lookups: {e}")
        return False


def parse_datetime(rowdate, rowtime):
    """
    Parses date and time strings into a datetime object.
    Supports multiple formats to handle inconsistencies.
    """
    if not rowdate:
        return None

    # Handle empty time
    if not rowtime:
        rowtime = "00:00"

    datetime_str = f"{rowdate} {rowtime}".strip()
    formats = [
        '%m/%d/%Y %H:%M:%S',
        '%m/%d/%Y %H:%M',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d',
        '%m/%d/%y %H:%M:%S',
        '%m/%d/%y %H:%M',
    ]
    for fmt in formats:
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue

    # If all formats fail, try to handle the date part only
    date_formats = ['%m/%d/%Y', '%Y-%m-%d', '%m/%d/%y']
    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(rowdate.strip(), fmt)
            # Add default time (noon) to avoid midnight issues
            return parsed_date.replace(hour=12)
        except ValueError:
            continue

    logger.warning(f"Failed to parse datetime: '{datetime_str}'")
    return None


def to_camel_case(s):
    """
    Converts a string to camelCase.
    Example: "SPECIFIC CONDUCTANCE" -> "specificConductance"
    """
    if not s:
        return ''
    parts = s.lower().split()
    if not parts:
        return ''
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def get_variable_type(medium_field):
    """
    Determine variable type based on the MEDIUM field value or return a default.
    """
    # Default to cached default or fallback
    default_type = constant_cache.get('default_variable_type')

    if not medium_field:
        return default_type

    if not isinstance(medium_field, str):
        logger.warning(f"Non-string medium_field: {medium_field}, type: {type(medium_field)}")
        return default_type

    medium_field = medium_field.strip().upper()

    # Mapping of medium values to variable types
    vartype_mapping = {
        'SEDIMENT': 'Sediment',
        'SOIL': 'Soil',
        'TISSUE': 'Tissue',
        'AIR': 'Air',
        'SOLID': 'Solid',
        'HABITAT': 'Habitat',
        'WATER': 'Water quality',  # Add water mapping
        'WATER QUALITY': 'Water quality',  # Add explicit water quality mapping
    }

    if medium_field in vartype_mapping:
        type_name = vartype_mapping[medium_field]

        # Check cache with both formats (with and without spaces)
        if type_name.lower() in constant_cache['variable_type_map']:
            return constant_cache['variable_type_map'][type_name.lower()]

        # Also try without spaces
        if type_name.lower().replace(' ', '') in constant_cache['variable_type_map']:
            return constant_cache['variable_type_map'][type_name.lower().replace(' ', '')]

        # Try to get from database with flexible matching
        try:
            cvvartype = CvVariabletype.objects.filter(
                Q(name__iexact=type_name) |
                Q(term__iexact=type_name.replace(' ', ''))
            ).first()

            if cvvartype:
                constant_cache['variable_type_map'][type_name.lower()] = cvvartype
                constant_cache['variable_type_map'][type_name.lower().replace(' ', '')] = cvvartype
                logger.info(f"Variable type set to '{cvvartype}'.")
                return cvvartype
        except Exception as e:
            logger.warning(f"Error getting variable type '{type_name}': {e}")

    # Return default
    return default_type

@db_retry(max_attempts=3)
def findCVVar(var):
    """
    Finds a CvVariablename object based on the variable name.
    Searches both 'name' and 'term' fields with enhanced matching logic.
    Returns the best match or None if no suitable match is found.
    """
    if not var:
        logger.error(f"Empty variable name provided to findCVVar")
        return None

    var_lower = var.lower()
    var_camel = to_camel_case(var)

    logger.info(f"Searching for CvVariablename matching: '{var}' (camelCase: '{var_camel}')")

    # Check the cache first
    if var_lower in constant_cache['cvvariablename_map']:
        logger.info(f"Found in cache: {constant_cache['cvvariablename_map'][var_lower]}")
        return constant_cache['cvvariablename_map'][var_lower]

    # 1. Exact case-insensitive match on 'name' or 'term'
    try:
        cvvars = CvVariablename.objects.filter(
            Q(name__iexact=var_lower) | Q(term__iexact=var_camel)
        )
        if cvvars.exists():
            if cvvars.count() == 1:
                result = cvvars.first()
                logger.info(f"Found exact match: {result}")
                constant_cache['cvvariablename_map'][var_lower] = result
                return result
            else:
                logger.warning(f"Multiple exact matches found for '{var}'. Selecting the first one.")
                result = cvvars.first()
                constant_cache['cvvariablename_map'][var_lower] = result
                return result
    except Exception as e:
        logger.error(f"Error during exact match lookup: {e}")

    # 2. Partial case-insensitive match on 'name' or 'term'
    try:
        cvvars = CvVariablename.objects.filter(
            Q(name__icontains=var_lower) | Q(term__icontains=var_camel)
        )
        if cvvars.exists():
            if cvvars.count() == 1:
                result = cvvars.first()
                logger.info(f"Found partial match: {result}")
                constant_cache['cvvariablename_map'][var_lower] = result
                return result
            else:
                logger.warning(f"Multiple partial matches found for '{var}'. Selecting the first one.")
                result = cvvars.first()
                constant_cache['cvvariablename_map'][var_lower] = result
                return result
    except Exception as e:
        logger.error(f"Error during partial match lookup: {e}")

    # 3. Attempt to find a match using varmap.csv
    try:
        with open('varmap.csv', 'r', newline='', encoding='utf-8') as mapfile:
            reader = csv.reader(mapfile)
            for row in reader:
                # Skip empty rows
                if not row or len(row) < 3:
                    continue
                # Assuming row[0] is the variable name and row[2] is the CvVariablename name
                if var_lower == row[0].lower():
                    try:
                        matched_var = CvVariablename.objects.filter(name__iexact=row[2].strip()).first()
                        if matched_var:
                            logger.info(f"Found match via varmap.csv: {matched_var}")
                            constant_cache['cvvariablename_map'][var_lower] = matched_var
                            return matched_var
                    except Exception as e:
                        logger.error(f"Error looking up match from varmap: {e}")
    except FileNotFoundError:
        logger.error("varmap.csv file not found. Skipping mapping-based search.")
    except Exception as e:
        logger.error(f"Error reading varmap.csv: {e}")

    # 4. Advanced Matching: Remove non-alphanumeric characters and retry
    try:
        var_clean = re.sub(r'\W+', '', var_lower)
        cvvars = CvVariablename.objects.filter(
            Q(name__icontains=var_clean) | Q(term__icontains=var_clean)
        )
        if cvvars.exists():
            if cvvars.count() == 1:
                result = cvvars.first()
                logger.info(f"Found advanced partial match: {result}")
                constant_cache['cvvariablename_map'][var_lower] = result
                return result
            else:
                logger.warning(f"Multiple advanced partial matches found for '{var}'. Selecting the first one.")
                result = cvvars.first()
                constant_cache['cvvariablename_map'][var_lower] = result
                return result
    except Exception as e:
        logger.error(f"Error during advanced matching: {e}")

    # 5. No match found
    logger.error(f"No CvVariablename match found for '{var}'.")
    return None


class RowProcessor:
    def __init__(self):
        # Caches to store previously retrieved Featureactions and Results
        self.featureaction_cache = {}
        self.results_cache = {}
        self.samplingfeatures_cache = {}
        self.sites_cache = {}
        self.variables_cache = {}
        self.units_cache = {}
        self.cache_lock = threading.Lock()

    def handle_results_creation(self, fa, newvar, newunit, row_number, lfile):
        """
        Handles the creation or retrieval of Results.
        Uses caching to reduce database queries and includes proper error handling.
        """
        try:
            # Define Results cache key
            results_cache_key = (fa.pk, newvar.pk, newunit.pk)

            with self.cache_lock:
                rs = self.results_cache.get(results_cache_key)

            if rs is None:
                # Query existing results with appropriate filters
                try:
                    rs_queryset = Results.objects.filter(
                        featureactionid=fa,
                        variableid=newvar,
                        unitsid=newunit
                    ).select_related('timeseriesresults')

                    # Convert queryset to list to avoid StopIteration errors
                    rs = list(rs_queryset)

                    if not rs:
                        # Get constants from cache instead of global variables
                        resulttype = constant_cache['resulttype']
                        plevel = constant_cache['processinglevels']
                        medium = constant_cache['medium']
                        if not resulttype or not plevel or not medium:
                            resulttype = CvResulttype.objects.get(name='Time series coverage')
                            plevel = Processinglevels.objects.get(processinglevelid=1)
                            medium = CvMedium.objects.get(name='Liquid aqueous')

                        logger.info(f"Row {row_number}: to create result use result type: {resulttype}")

                        # Validate all required values exist
                        if not resulttype or not plevel or not medium:
                            raise ValueError("Missing required constant values for Result creation")

                        # Create a new Result with a transaction
                        with transaction.atomic():
                            new_result = Results.objects.create(
                                featureactionid=fa,
                                result_type=resulttype,
                                variableid=newvar,
                                unitsid=newunit,
                                processing_level=plevel,
                                sampledmediumcv=medium,
                                valuecount=1
                            )

                        logger.info(f"Row {row_number}: Created new Result: {new_result}")
                        lfile.write(f"Row {row_number}: Created new Result: {new_result}\n")

                        # Add to list for return
                        rs = [new_result]
                    else:
                        logger.info(f"Row {row_number}: Found {len(rs)} existing Results")

                    # Add to cache
                    with self.cache_lock:
                        self.results_cache[results_cache_key] = rs

                except IntegrityError as e:
                    logger.error(f"Row {row_number}: Database integrity error creating Result: {e}")
                    lfile.write(f"Row {row_number}: Database integrity error creating Result: {e}\n")
                    return None
                except Exception as e:
                    logger.error(f"Row {row_number}: Unexpected error handling Results: {e}")
                    lfile.write(f"Row {row_number}: Unexpected error handling Results: {e}\n")
                    return None
            else:
                logger.debug(f"Row {row_number}: Results retrieved from cache for key {results_cache_key}.")

            return rs

        except Exception as e:
            logger.error(f"Row {row_number}: Critical error in Results handling: {e}")
            lfile.write(f"Row {row_number}: Critical error in Results handling: {e}\n")
            return None

    def process_row(self, row, row_number, lfile, filename, baddateonly, stopatdupvalue):
        """
        Processes an individual row from the CSV file.
        Handles data validation, transformation, and database insertion.
        """
        try:
            # -------------------------
            # 1. Data Extraction & Validation
            # -------------------------
            parameter_analyte = row.get(PARAMETER_ANALYTE, '').strip()
            if not parameter_analyte or parameter_analyte.upper() == 'PARAMETER/ANALYTE':
                # Skip header row or handle accordingly
                logger.debug(f"Row {row_number}: Skipping header or empty row.")
                return

            qualifier_results = row.get(QUALIFIER_RESULTS, '').strip()
            units = row.get(UNITS, '').strip().lower()
            result_valid = row.get(RESULT_VALID, '').strip().lower()
            rowdate = row.get(START_DATE, '').strip()
            rowtime = row.get(START_TIME, '').strip()

            # Parse datetime
            datet = parse_datetime(rowdate, rowtime)
            if not datet:
                logger.warning(f"Row {row_number}: Invalid datetime '{rowdate} {rowtime}' in '{filename}'.")
                if baddateonly:
                    return

            # Adjust datetime if time indicates midnight
            if rowtime in ['0:00', '00:00', '00:00:00']:
                datet += timedelta(hours=12)
                logger.info(f"Row {row_number}: Adjusted datetime by adding 12 hours.")

            # Determine value validity
            valuevalid, baddata, unknown, preliminary = self.determine_validity(result_valid)

            if not valuevalid:
                logger.warning(f"Row {row_number}: Invalid 'RESULT VALID' value '{result_valid}'.")
                return

            # Find the standard variable from the database
            stdvar = findCVVar(parameter_analyte)
            if not stdvar:
                logger.error(f"Row {row_number}: Variable '{parameter_analyte}' not found.")
                lfile.write(f"Row {row_number}: Variable '{parameter_analyte}' not found.\n")
                return

            # Find Variable Type
            vartype_field = row.get(MEDIUM, '').strip()  # Use MEDIUM instead of DEPTH_ZONE
            cvvartype = get_variable_type(vartype_field)

            if not cvvartype:
                logger.error(f"Row {row_number}: Default CvVariabletype 'Water quality' not found.")
                lfile.write(f"Row {row_number}: Default CvVariabletype 'Water quality' not found.\n")
                return

            # Attempt to retrieve the Variable object
            var_cache_key = (stdvar.pk, cvvartype.pk)
            with self.cache_lock:
                newvar = self.variables_cache.get(var_cache_key)

            if not newvar:
                try:
                    # Ensure that the field names match your Django models
                    newvar_queryset = Variables.objects.filter(
                        variable_name=stdvar,
                        variable_type=cvvartype
                    )
                    newvar = newvar_queryset.first()

                    if newvar:
                        if newvar_queryset.count() > 1:
                            logger.warning(
                                f"Row {row_number}: Multiple Variables found with name '{stdvar}' and type '{cvvartype}'. Using the first one: '{newvar}'.")
                        else:
                            logger.info(f"Row {row_number}: Retrieved Variable: {newvar}")

                        with self.cache_lock:
                            self.variables_cache[var_cache_key] = newvar
                    else:
                        logger.error(
                            f"Row {row_number}: Variable with name '{stdvar}' and type '{cvvartype}' not found.")
                        lfile.write(
                            f"Row {row_number}: Variable with name '{stdvar}' and type '{cvvartype}' not found.\n")
                        return
                except Exception as e:
                    logger.error(f"Row {row_number}: Unexpected error retrieving Variable: {e}")
                    lfile.write(f"Row {row_number}: Unexpected error retrieving Variable: {e}\n")
                    return

            # -------------------------
            # 2. Samplingfeature and Site Retrieval
            # -------------------------
            samplingfeaturecode = row.get(STATION_ID, '').strip().upper()
            if not samplingfeaturecode:
                logger.warning(f"Row {row_number}: Missing STATION ID. Skipping.")
                return

            try:
                with self.cache_lock:
                    newsf = self.samplingfeatures_cache.get(samplingfeaturecode)

                if not newsf:
                    newsf = Samplingfeatures.objects.get(samplingfeaturecode__iexact=samplingfeaturecode)
                    logger.info(f"Row {row_number}: Retrieved Samplingfeatures: {newsf}")

                    with self.cache_lock:
                        self.samplingfeatures_cache[samplingfeaturecode] = newsf
            except Samplingfeatures.DoesNotExist:
                logger.error(f"Row {row_number}: Samplingfeature with code '{samplingfeaturecode}' not found.")
                lfile.write(f"Row {row_number}: Samplingfeature with code '{samplingfeaturecode}' not found.\n")
                return
            except Exception as e:
                logger.error(f"Row {row_number}: Unexpected error retrieving Samplingfeatures: {e}")
                lfile.write(f"Row {row_number}: Unexpected error retrieving Samplingfeatures: {e}\n")
                return

            # Verify if associated Site exists
            try:
                with self.cache_lock:
                    existing_site = self.sites_cache.get(newsf.pk)

                if not existing_site:
                    existing_site = Sites.objects.get(samplingfeatureid=newsf)
                    logger.info(f"Row {row_number}: Retrieved existing Site: {existing_site}")

                    with self.cache_lock:
                        self.sites_cache[newsf.pk] = existing_site
            except Sites.DoesNotExist:
                logger.error(f"Row {row_number}: Site associated with Samplingfeature '{newsf}' not found.")
                lfile.write(f"Row {row_number}: Site associated with Samplingfeature '{newsf}' not found.\n")
                return
            except Exception as e:
                logger.error(f"Row {row_number}: Unexpected error retrieving Site: {e}")
                lfile.write(f"Row {row_number}: Unexpected error retrieving Site: {e}\n")
                return

            # -------------------------
            # 3. Actiontype Retrieval
            # -------------------------
            try:
                actiontype = CvActiontype.objects.get(name='Specimen analysis')
                logger.info(f"Row {row_number}: Retrieved Actiontype: {actiontype}")
            except CvActiontype.DoesNotExist:
                logger.error(f"Row {row_number}: Action type 'Specimen analysis' does not exist.")
                lfile.write(f"Row {row_number}: Action type 'Specimen analysis' does not exist.\n")
                return
            except Exception as e:
                logger.error(f"Row {row_number}: Unexpected error retrieving Action type: {e}")
                lfile.write(f"Row {row_number}: Unexpected error retrieving Action type: {e}\n")
                return
            # -------------------------
            # 4. Featureactions Retrieval with Caching and Creation
            # -------------------------
            cache_key = (newsf.pk, actiontype.pk)
            with self.cache_lock:
                fas = self.featureaction_cache.get(cache_key)

            if fas is None:
                try:
                    detectionlimit = ''
                    if row.get(RDL):
                        detectionlimit = f" Reporting Limit (RDL): {row.get(RDL)} {row.get(DETECTION_LIMIT, '')} {row.get(DETECTION_LIMIT_COMMENTS, '')}"

                    methdesc = (
                        f"NHDES grab-sample method: {row.get(ANALYTICAL_METHOD, '').strip().lower().title()} "
                        f"- lab: {row.get(LAB_ID, '').strip()} "
                        f"- analytical method source: {row.get(ANALYTICAL_METHOD_SOURCE_ID, '').strip().lower().title()}"
                    ) + ' ' + detectionlimit

                    fas_queryset = Featureactions.objects.filter(
                        samplingfeatureid=newsf,
                        action__action_type=actiontype,
                        action__method__methoddescription__istartswith=methdesc
                    ).select_related('action__method')

                    fas = list(fas_queryset)
                    if not fas:
                        logger.warning(
                            f"Row {row_number}: No Featureactions matching criteria found for Samplingfeature '{newsf}'. Creating a new Featureaction.")
                        lfile.write(
                            f"Row {row_number}: No Featureactions matching criteria found for Samplingfeature '{newsf}'. Creating a new Featureaction.\n")

                        # -------------------------
                        # Create Method
                        # -------------------------
                        method_description = methdesc
                        method_type = constant_cache.get('methtype')
                        if not method_type:
                            method_type = CvMethodtype.objects.get(name='Specimen analysis')
                            if not method_type:
                                logger.error(f"Row {row_number}: Method type is not defined in constant_cache")
                                return  # Skip to the next record if method type is not available

                        method = Methods.objects.filter(methoddescription__iexact=method_description).first()
                        # If no method found, create one
                        if not method:
                            method = Methods.objects.create(
                                methoddescription=method_description,
                                methodtypecv=method_type
                            )
                            created = True
                            logger.info(f"Row {row_number}: Created new Method: {method}")
                            lfile.write(f"Row {row_number}: Created new Method: {method}\n")
                        else:
                            created = False
                            logger.info(f"Row {row_number}: Retrieved existing Method: {method}")
                        # -------------------------
                        # Create Action
                        # -------------------------
                        station_name = row.get(STATION_NAME, '').strip().lower().title()
                        activity_id = row.get(ACTIVITY_ID, '').strip().lower().title()
                        activity_type = row.get(ACTIVITY_TYPE, '').strip().lower().title()

                        action_description = f"{samplingfeaturecode} {station_name} {activity_id} {activity_type}"

                        # Similar approach for the action
                        action = Actions.objects.filter(actiondescription__iexact=action_description).first()
                        if not action:
                            action = Actions.objects.create(
                                actiondescription=action_description,
                                action_type=actiontype,
                                method=method,
                                begindatetime=datet
                            )
                            logger.info(f"Row {row_number}: Created new Action: {action}")
                            lfile.write(f"Row {row_number}: Created new Action: {action}\n")
                        else:
                            logger.info(f"Row {row_number}: Retrieved existing Action: {action}")

                        # -------------------------
                        # Create Featureaction
                        # -------------------------
                        featureaction = Featureactions.objects.create(
                            samplingfeatureid=newsf,
                            action=action
                        )
                        fas = [featureaction]
                        with self.cache_lock:
                            self.featureaction_cache[cache_key] = fas

                        logger.info(f"Row {row_number}: Created new Featureaction: {featureaction}")
                        lfile.write(f"Row {row_number}: Created new Featureaction: {featureaction}\n")
                    else:
                        with self.cache_lock:
                            self.featureaction_cache[cache_key] = fas

                        logger.info(
                            f"Row {row_number}: Retrieved and cached {len(fas)} Featureactions for Samplingfeature '{newsf}'.")
                except Exception as e:
                    logger.error(f"Row {row_number}: Unexpected error retrieving or creating Featureactions: {e}")
                    lfile.write(f"Row {row_number}: Unexpected error retrieving or creating Featureactions: {e}\n")
                    return
            else:
                logger.debug(f"Row {row_number}: Featureactions retrieved from cache for key {cache_key}.")

            # -------------------------
            # 5. Units Retrieval
            # -------------------------
            unit_abbreviation = units
            try:
                newunit = Units.objects.get(unitsabbreviation__iexact=unit_abbreviation)
                logger.info(f"Row {row_number}: Retrieved Unit: {newunit}")
            except Units.DoesNotExist:
                logger.error(f"Row {row_number}: Unit with abbreviation '{unit_abbreviation}' not found.")
                lfile.write(f"Row {row_number}: Unit with abbreviation '{unit_abbreviation}' not found.\n")
                return
            except MultipleObjectsReturned:
                logger.error(f"Row {row_number}: Multiple Units found with abbreviation '{unit_abbreviation}'. Selecting the first one.")
                newunit = Units.objects.filter(unitsabbreviation__iexact=unit_abbreviation).first()
                if newunit:
                    logger.info(f"Row {row_number}: Selected first Unit: {newunit}")
                else:
                    logger.error(f"Row {row_number}: No Units found after handling multiple entries for abbreviation '{unit_abbreviation}'.")
                    lfile.write(f"Row {row_number}: No Units found after handling multiple entries for abbreviation '{unit_abbreviation}'.\n")
                    return
            except Exception as e:
                logger.error(f"Row {row_number}: Unexpected error retrieving Unit: {e}")
                lfile.write(f"Row {row_number}: Unexpected error retrieving Unit: {e}\n")
                return

            # -------------------------
            # 6. Handling Results and Timeseries within an Atomic Transaction
            # -------------------------
            with transaction.atomic():
                for fa in fas:
                    try:
                        # Get or create Results
                        rs = self.handle_results_creation(fa, newvar, newunit, row_number, lfile)

                        if not rs:
                            continue  # Skip to the next Featureaction if we couldn't get Results

                        for r in rs:
                            try:
                                # Try to get existing Timeseriesresults
                                try:
                                    tsr = Timeseriesresults.objects.get(resultid=r)
                                    logger.info(
                                        f"Row {row_number}: Retrieved Timeseriesresults: {tsr} for Result '{r}'.")
                                except Timeseriesresults.DoesNotExist:
                                    # Create Timeseriesresults
                                    tsr = self.create_timeseriesresults(row, r, row_number, filename, stopatdupvalue,
                                                                        logger)
                                    if not tsr:
                                        continue  # Skip to the next Result
                                except Exception as e:
                                    logger.error(
                                        f"Row {row_number}: Unexpected error retrieving Timeseriesresults for Result '{r}': {e}",
                                        exc_info=True)
                                    lfile.write(
                                        f"Row {row_number}: Unexpected error retrieving Timeseriesresults for Result '{r}': {e}\n")
                                    continue
                                aggstat = CvAggregationstatistic.objects.get(name='Continuous')
                                # Create Timeseriesresultvalues
                                self.handle_timeseriesresultvalues(
                                    row=row,
                                    tsr=tsr,
                                    datet=datet,
                                    aggstat=aggstat,  # Use cached value
                                    lfile=lfile,
                                    row_number=row_number,
                                    filename=filename,
                                    baddata=baddata,
                                    unknown=unknown,
                                    preliminary=preliminary,
                                    stopatdupvalue=stopatdupvalue
                                )

                            except Exception as e:
                                logger.error(f"Row {row_number}: Error processing Result {r}: {e}")
                                lfile.write(f"Row {row_number}: Error processing Result {r}: {e}\n")
                                continue  # Continue to next Result

                    except Exception as e:
                        logger.error(f"Row {row_number}: Error processing Featureaction {fa}: {e}")
                        lfile.write(f"Row {row_number}: Error processing Featureaction {fa}: {e}\n")
                        continue  # Continue to next Featureaction
        except Exception as e:
            logger.error(f"Row {row_number}: Critical error processing row: {e}")
            lfile.write(f"Row {row_number}: Critical error processing row: {e}\n")
            return

    def create_timeseriesresults(self, row, result, row_number, filename, stopatdupvalue, logger):
        """
        Creates a Timeseriesresults instance for a given Result.
        """
        try:
            zlocation_units_abbr = row.get(DEPTH_UNITS, '').strip().lower()
            zlocation_units = Units.objects.get(unitsabbreviation__iexact=zlocation_units_abbr)
            zlocation_raw = row.get(DEPTH, '').strip()
            zlocation = float(zlocation_raw) if zlocation_raw else None
            aggstat = CvAggregationstatistic.objects.get(name='Continuous')
            tsr = Timeseriesresults.objects.create(
                resultid=result,
                aggregationstatisticcv=aggstat,
                zlocationunitsid=zlocation_units,
                zlocation=zlocation
            )
            logger.info(f"Row {row_number}: Created Timeseriesresults: {tsr}")
            return tsr
        except Units.DoesNotExist:
            logger.error(f"Row {row_number}: Units with abbreviation '{zlocation_units_abbr}' not found.")
            return None
        except ValueError:
            logger.error(f"Row {row_number}: Invalid z-location value '{row.get(DEPTH, '').strip()}'.")
            return None
        except IntegrityError as e:
            logger.error(f"Row {row_number}: IntegrityError creating Timeseriesresults: {e}")
            if stopatdupvalue:
                raise e
            return None
        except Exception as e:
            logger.error(f"Row {row_number}: Unexpected error creating Timeseriesresults: {e}")
            return None

    def clean_numeric(self, value):
        """
        Cleans and converts a string to a float.
        - Removes leading operators like '=', '<', '>', '<=', '>='.
        - Extracts the first float-like pattern.
        - Returns None if no valid number is found.
        """
        if not value:
            return None

        # Remove leading operators and strip whitespace
        value = re.sub(r'^[<>=]+', '', value).strip()

        # Use regex to find the first float or integer
        match = re.search(r'[-+]?\d*\.?\d+', value)
        if match:
            try:
                return float(match.group())
            except ValueError:
                return None
        return None

    def determine_validity(self, result_valid):
        """
        Determines the validity of the result based on the 'RESULT VALID' field.

        Parameters:
        - result_valid: String indicating the validity.

        Returns:
        - Tuple (valuevalid, baddata, unknown, preliminary)
        """
        valuevalid = False
        baddata = False
        unknown = False
        preliminary = False

        if result_valid in ['y', 'yes', 'final']:
            valuevalid = True
        elif result_valid == 'preliminary':
            valuevalid = True
            preliminary = True
        elif result_valid in ['n', 'no']:
            baddata = True
            valuevalid = True
        elif result_valid == 'unknown':
            unknown = True
            valuevalid = True

        return valuevalid, baddata, unknown, preliminary

    @db_retry(max_attempts=3, delay=2)
    def handle_timeseriesresultvalues(self, row, tsr, datet, aggstat, lfile, row_number, filename, baddata, unknown, preliminary, stopatdupvalue):
        """
        Handles the creation of Timeseriesresultvalues and associated annotations.
        """
        # Parse and clean the value
        val_raw = row.get(QUALIFIER_RESULTS, '').strip()
        val = self.clean_numeric(val_raw)

        if val is None:
            if 'unknown' in val_raw.lower():
                unknown = True
            else:
                logger.warning(f"Row {row_number}: Invalid data value '{val_raw}'.")
                lfile.write(f"Row {row_number}: Invalid data value '{val_raw}'.\n")
                return  # Skip to the next Result

        # Handle censoring and quality codes
        try:
            if baddata:
                quality = CvQualitycode.objects.get(name="Bad")
            elif unknown:
                quality = CvQualitycode.objects.get(name="Unknown")
            elif preliminary:
                quality = CvQualitycode.objects.get(name="Pending QA")
            else:
                quality = CvQualitycode.objects.get(name="Good")
            logger.info(f"Row {row_number}: Assigned Quality Code: {quality}")
        except CvQualitycode.DoesNotExist as e:
            logger.error(f"Row {row_number}: Quality code not found: {e}")
            lfile.write(f"Row {row_number}: Quality code not found: {e}.\n")
            return

        try:
            censorcode = CvCensorcode.objects.get(name="Not censored")
            logger.info(f"Row {row_number}: Assigned Censor Code: {censorcode}")
        except CvCensorcode.DoesNotExist:
            logger.error(f"Row {row_number}: Censor code 'Not censored' not found.")
            lfile.write(f"Row {row_number}: Censor code 'Not censored' not found.\n")
            return
        except Exception as e:
            logger.error(f"Row {row_number}: Unexpected error retrieving Censor code: {e}")
            lfile.write(f"Row {row_number}: Unexpected error retrieving Censor code: {e}\n")
            return

        try:
            newtimeunit = Units.objects.get(unitsname__iexact='minute')
            logger.info(f"Row {row_number}: Assigned Time Aggregation Unit: {newtimeunit}")
        except Units.DoesNotExist:
            logger.error(f"Row {row_number}: Time unit 'minute' not found.")
            lfile.write(f"Row {row_number}: Time unit 'minute' not found.\n")
            return
        except Exception as e:
            logger.error(f"Row {row_number}: Unexpected error retrieving Time unit: {e}")
            lfile.write(f"Row {row_number}: Unexpected error retrieving Time unit: {e}\n")
            return

        # Create or get Timeseriesresultvalues
        try:
            tsrv, created = Timeseriesresultvalues.objects.get_or_create(
                resultid=tsr,
                valuedatetime=datet,
                defaults={
                    'datavalue': val,
                    'valuedatetimeutcoffset': -5,
                    'censorcodecv': censorcode,
                    'qualitycodecv': quality,
                    'timeaggregationinterval': 1,
                    'timeaggregationintervalunitsid': newtimeunit
                }
            )
            if created:
                logger.info(f"Row {row_number}: Created Timeseriesresultvalue: {tsrv}")
                lfile.write(f"Row {row_number}: Created Timeseriesresultvalue: {tsrv}\n")
            else:
                logger.warning(f"Row {row_number}: Timeseriesresultvalue already exists: {tsrv}")
                if stopatdupvalue:
                    return
        except IntegrityError as e:
            logger.error(f"Row {row_number}: IntegrityError creating Timeseriesresultvalue: {e}")
            lfile.write(f"Row {row_number}: IntegrityError creating Timeseriesresultvalue: {e}\n")
            if stopatdupvalue:
                raise e  # Stop processing if flag is set
            return  # Skip to the next Result
        except Exception as e:
            logger.error(f"Row {row_number}: Unexpected error creating Timeseriesresultvalue: {e}")
            lfile.write(f"Row {row_number}: Unexpected error creating Timeseriesresultvalue: {e}\n")
            return  # Skip to the next Result

        # Handle Annotations if needed
        annotation_text = []
        annotation_code = []

        if "<" in row.get(QUALIFIER_RESULTS, ''):
            annotation_text.append(f"Below detection limit of {row.get(QUALIFIER_RESULTS, '').strip()}")
            annotation_code.append("Below detection limit")

        if ">" in row.get(QUALIFIER_RESULTS, ''):
            annotation_text.append(f"Above method detection maximum of {row.get(QUALIFIER_RESULTS, '').strip()}")
            annotation_code.append("Above method detection maximum")

        result_comments = row.get(RESULT_COMMENTS, '').strip()
        if result_comments:
            annotation_text.append(f"Result comment: {result_comments}")
            annotation_code.append("Result comment")

        depth_raw = row.get(DEPTH, '').strip()
        depth = self.clean_numeric(depth_raw)
        depth_units = row.get(DEPTH_UNITS, '').strip().lower()
        if depth is not None:
            annotation_text.append(f"Depth of sample: {depth} {depth_units}")
            annotation_code.append("Depth of sample")

        activity_id = row.get(ACTIVITY_ID, '').strip()
        if activity_id:
            annotation_text.append(f"Sample ID: {activity_id}")
            annotation_code.append("Sample ID")

        if annotation_text:
            annotation_text_combined = " -- ".join(annotation_text)
            annotation_code_combined = " -- ".join(annotation_code)[:50]  # Truncate to 50 characters

            try:
                annotationtype = CvAnnotationtype.objects.get(name="Time series result value annotation")
                logger.info(f"Row {row_number}: Retrieved Annotation Type: {annotationtype}")
            except CvAnnotationtype.DoesNotExist:
                logger.error(f"Row {row_number}: Annotation type 'Time series result value annotation' not found.")
                lfile.write(f"Row {row_number}: Annotation type 'Time series result value annotation' not found.\n")
                return  # Skip to the next Result
            except Exception as e:
                logger.error(f"Row {row_number}: Unexpected error retrieving Annotation type: {e}")
                lfile.write(f"Row {row_number}: Unexpected error retrieving Annotation type: {e}\n")
                return  # Skip to the next Result

            try:
                annotator = People.objects.get(personid=1)  # Ensure personid=1 exists
                logger.info(f"Row {row_number}: Retrieved Annotator: {annotator}")
            except People.DoesNotExist:
                logger.error(f"Row {row_number}: Annotator with personid=1 not found.")
                lfile.write(f"Row {row_number}: Annotator with personid=1 not found.\n")
                return  # Skip to the next Result
            except Exception as e:
                logger.error(f"Row {row_number}: Unexpected error retrieving Annotator: {e}")
                lfile.write(f"Row {row_number}: Unexpected error retrieving Annotator: {e}\n")
                return  # Skip to the next Result

            try:
                annotation, created = Annotations.objects.get_or_create(
                    annotationtypecv=annotationtype,
                    annotationcode=annotation_code_combined,
                    annotationtext=annotation_text_combined,
                    annotationdatetime=datetime.now(),
                    annotationlink=activity_id,
                    annotationutcoffset=4,
                    annotatorid=annotator
                )
                if created:
                    logger.info(f"Row {row_number}: Created Annotation: {annotation}")
                    lfile.write(f"Row {row_number}: Created Annotation: {annotation}\n")
                else:
                    logger.warning(f"Row {row_number}: Annotation already exists: {annotation}")

                # Associate Annotation with Timeseriesresultvalue
                Timeseriesresultvalueannotations.objects.get_or_create(
                    valueid=tsrv,
                    annotationid=annotation
                )
                logger.info(f"Row {row_number}: Associated Annotation '{annotation}' with Timeseriesresultvalue '{tsrv}'.")
                lfile.write(f"Row {row_number}: Associated Annotation '{annotation}' with Timeseriesresultvalue '{tsrv}'.\n")
            except IntegrityError as e:
                logger.error(f"Row {row_number}: IntegrityError while creating annotation: {e}")
                lfile.write(f"Row {row_number}: IntegrityError while creating annotation: {e}\n")
                if stopatdupvalue:
                    raise e  # Stop processing if flag is set
                return  # Skip to the next Result
            except Exception as e:
                logger.error(f"Row {row_number}: Unexpected error creating annotation: {e}")
                lfile.write(f"Row {row_number}: Unexpected error creating annotation: {e}\n")
                return  # Skip to the next Result

        logger.debug(f"Row {row_number}: Successfully processed Timeseriesresultvalue and annotations.")


def loadgrabdata(directory, filename, baddateonly=False, stopatdupvalue=False):
    """
    Main function to load grab data from a file.
    Converts Excel files to CSV and processes CSV files.
    """
    processor = RowProcessor()
    file_path = os.path.join(directory, filename)

    try:
        if filename.lower().endswith(".xlsx"):
            logger.info(f"Converting Excel file '{filename}' to CSV")
            csv_filename = os.path.splitext(filename)[0] + '.csv'
            csv_path = os.path.join(directory, csv_filename)

            # Convert Excel to CSV
            convert_xlsx_to_csv(directory, filename)

            # Verify the CSV was created
            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"Failed to create CSV file from '{filename}'")

            logger.info(f"Successfully converted '{filename}' to '{csv_filename}'")
            # Process the newly created CSV
            process_csv_file(directory, csv_filename, processor, baddateonly, stopatdupvalue)

        elif filename.lower().endswith(".csv"):
            logger.info(f"Processing CSV file '{filename}'")
            process_csv_file(directory, filename, processor, baddateonly, stopatdupvalue)

        else:
            logger.warning(f"Unsupported file format for '{filename}'. Skipping.")

    except Exception as e:
        logger.error(f"Error processing file '{filename}': {e}", exc_info=True)
        with open(f'loggrabsamples_a{filename}.log', 'a') as lfile:
            lfile.write(f"ERROR processing file '{filename}': {e}\n")


def convert_xlsx_to_csv(directory, filename):
    """
    Converts an Excel file to a CSV file by reading multiple possible sheets.
    Enhanced to handle different column structures.
    """
    filepath = os.path.join(directory, filename)
    sheets = [
        'GrabSample_PhysChem_StationID',
        'GrabSample_Bio_WaterbodyID',
        'GrabSample_PhysChem_RiverName',
        'GrabSample_PhysChem_WaterbodyID',
        'GrabSample_PhysChem_Project',
        'GrabSample_PhysChem_Parameter'
    ]

    data_xls = None
    sheet_found = None

    for sheet in sheets:
        try:
            # Try to read with header at row 4 first
            try:
                data_xls = pd.read_excel(filepath, sheet_name=sheet, header=4)
                sheet_found = sheet
                logger.info(f"Successfully read sheet '{sheet}' from '{filename}' with header at row 4")
                break
            except Exception as e1:
                # If that fails, try with auto header detection
                try:
                    data_xls = pd.read_excel(filepath, sheet_name=sheet)
                    sheet_found = sheet
                    logger.info(f"Successfully read sheet '{sheet}' from '{filename}' with auto header detection")
                    break
                except Exception as e2:
                    logger.warning(f"Failed to read sheet '{sheet}' from '{filename}': {e1}, {e2}")
                    continue
        except Exception as e:
            logger.warning(f"Failed to read sheet '{sheet}' from '{filename}': {e}")
            continue

    if data_xls is None:
        raise ValueError(f"No valid sheet found in '{filename}'. Available sheets: {sheets}")

    # Log the columns found in the Excel file
    logger.info(f"Columns found in Excel file: {list(data_xls.columns)}")

    # Check for required columns
    required_columns = [PARAMETER_ANALYTE, STATION_ID, START_DATE, QUALIFIER_RESULTS, UNITS]
    missing_columns = [col for col in required_columns if col not in data_xls.columns]

    if missing_columns:
        logger.warning(f"Missing required columns in '{filename}': {missing_columns}")

        # Try to match column names case-insensitively
        column_map = {}
        for required in missing_columns:
            for actual in data_xls.columns:
                if required.lower() == actual.lower():
                    column_map[actual] = required
                    logger.info(f"Mapped column '{actual}' to '{required}'")

        # Rename columns if matches found
        if column_map:
            data_xls = data_xls.rename(columns=column_map)
            # Update missing columns list
            missing_columns = [col for col in required_columns if col not in data_xls.columns]

        if missing_columns:
            logger.error(f"Still missing required columns after mapping: {missing_columns}")

    # Convert date and time columns if they exist
    try:
        if START_DATE in data_xls.columns:
            data_xls[START_DATE] = pd.to_datetime(data_xls[START_DATE], errors='coerce')
        if START_TIME in data_xls.columns:
            data_xls[START_TIME] = pd.to_datetime(data_xls[START_TIME], errors='coerce').dt.time
    except Exception as e:
        logger.warning(f"Error converting date/time columns in '{filename}': {e}")

    # Save as CSV
    newfilepath = os.path.splitext(filepath)[0] + '.csv'
    try:
        # Use UTF-8 encoding and tab delimiter for consistency
        data_xls.to_csv(newfilepath, encoding='utf-8', index=False, sep='\t')
        logger.info(f"Successfully converted '{filename}' (sheet: '{sheet_found}') to CSV: '{newfilepath}'")
    except Exception as e:
        raise Exception(f"Failed to convert '{filename}' to CSV: {e}")


@db_retry(max_attempts=3)
def handle_featureaction_creation(self, newsf, actiontype, methdesc, datet, activity_data, row_number, lfile):
    """
    Handle creation of Featureaction with proper method handling.
    """
    try:
        # Find existing method instead of using get() which fails on multiple results
        method = Methods.objects.filter(
            methoddescription__iexact=methdesc
        ).first()

        if not method:
            # Create method if it doesn't exist
            method_type = constant_cache.get('methtype')
            if not method_type:
                method_type = CvMethodtype.objects.get(name='Specimen analysis')

            method = Methods.objects.create(
                methoddescription=methdesc,
                methodtypecv=method_type
            )
            logger.info(f"Row {row_number}: Created new Method: {method}")
            lfile.write(f"Row {row_number}: Created new Method: {method}\n")
        else:
            logger.info(f"Row {row_number}: Retrieved existing Method: {method}")

        # Create Action
        action_description = f"{activity_data['samplingfeaturecode']} {activity_data['station_name']} {activity_data['activity_id']} {activity_data['activity_type']}"

        action = Actions.objects.filter(
            actiondescription__iexact=action_description
        ).first()

        if not action:
            action = Actions.objects.create(
                actiondescription=action_description,
                action_type=actiontype,
                method=method,
                begindatetime=datet
            )
            logger.info(f"Row {row_number}: Created new Action: {action}")
            lfile.write(f"Row {row_number}: Created new Action: {action}\n")
        else:
            logger.info(f"Row {row_number}: Retrieved existing Action: {action}")

        # Create Featureaction
        featureaction = Featureactions.objects.create(
            samplingfeatureid=newsf,
            action=action
        )
        logger.info(f"Row {row_number}: Created new Featureaction: {featureaction}")
        lfile.write(f"Row {row_number}: Created new Featureaction: {featureaction}\n")

        return [featureaction]
    except Exception as e:
        logger.error(f"Row {row_number}: Error creating Featureaction: {e}")
        lfile.write(f"Row {row_number}: Error creating Featureaction: {e}\n")
        return None

def process_csv_file(directory, filename, processor, baddateonly, stopatdupvalue):
    """
    Processes a CSV file by reading each row and handling data insertion.
    Improved to handle variable column structure and None values.
    """
    filepath = os.path.join(directory, filename)
    logger.info(f"Processing CSV file: '{filename}'.")

    # First check if file exists and is readable
    if not os.path.isfile(filepath):
        logger.error(f"File not found: '{filepath}'")
        return

    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as tempfile, open(f'loggrabsamples_a{filename}.log',
                                                                                 'a') as lfile:
            # Read the first few lines to inspect the structure
            header_check = []
            for i in range(10):  # Read up to 10 lines
                try:
                    line = next(tempfile)
                    header_check.append(line)
                except StopIteration:
                    break

            # Reset file pointer to beginning
            tempfile.seek(0)

            # Try to detect the actual columns in the file
            try:
                dialect = csv.Sniffer().sniff(''.join(header_check[:3]), delimiters=',\t;')
                reader = csv.reader(tempfile, dialect)
                header = next(reader)

                # Log the detected columns for debugging
                logger.info(f"Detected {len(header)} columns in '{filename}'.")
                if header:
                    logger.info(f"First few columns: {header[:5]}")

                # Create a new reader that treats the first row as header
                tempfile.seek(0)
                reader = csv.DictReader(tempfile, dialect=dialect)

            except Exception as e:
                logger.warning(f"Could not detect CSV format: {e}. Falling back to tab delimiter.")
                tempfile.seek(0)
                reader = csv.DictReader(tempfile, delimiter='\t')

            # Process each row
            for i, row in enumerate(reader, start=1):
                try:
                    # Validate required fields are present and not None
                    required_fields = [PARAMETER_ANALYTE, STATION_ID, START_DATE]
                    missing_fields = []

                    for field in required_fields:
                        if field not in row:
                            missing_fields.append(field)
                        elif row[field] is None:
                            missing_fields.append(f"{field} (None)")
                        elif not str(row[field]).strip():
                            missing_fields.append(f"{field} (Empty)")

                    if missing_fields:
                        logger.warning(f"Row {i} is missing required fields: {', '.join(missing_fields)}. Skipping.")
                        continue

                    # Check if PARAMETER_ANALYTE is header-like
                    param_value = str(row.get(PARAMETER_ANALYTE, '')).strip()
                    if param_value.upper() == 'PARAMETER/ANALYTE':
                        logger.warning(f"Row {i} contains header. Skipping.")
                        continue

                    # Create a safe row with string values and empty string fallbacks
                    safe_row = {}
                    for key, value in row.items():
                        if value is None:
                            safe_row[key] = ''
                        else:
                            safe_row[key] = str(value)

                    processor.process_row(safe_row, i, lfile, filename, baddateonly, stopatdupvalue)

                except StopIteration:
                    logger.error(f"StopIteration error at row {i}. CSV may be malformed.")
                    lfile.write(f"ERROR: StopIteration at row {i}. CSV may be malformed.\n")
                    break
                except KeyError as e:
                    logger.error(f"Column missing in row {i}: {e}")
                    lfile.write(f"ERROR: Column missing in row {i}: {e}\n")
                    continue
                except Exception as e:
                    logger.error(f"Error processing row {i} in '{filename}': {e}", exc_info=True)
                    lfile.write(f"ERROR processing row {i} in '{filename}': {e}\n")
                    continue

    except UnicodeDecodeError:
        logger.error(f"Character encoding issue in '{filename}'. Attempting with different encoding...")
        # Try alternative encodings
        try_encodings = ['latin-1', 'windows-1252', 'utf-16']
        for encoding in try_encodings:
            try:
                with open(filepath, 'r', newline='', encoding=encoding) as tempfile, open(
                        f'loggrabsamples_a{filename}.log', 'a') as lfile:
                    lfile.write(f"Retrying with {encoding} encoding\n")
                    # Same CSV processing code with encoding
                    reader = csv.DictReader(tempfile, delimiter='\t')
                    for i, row in enumerate(reader, start=1):
                        try:
                            # Create safe row
                            safe_row = {}
                            for key, value in row.items():
                                if value is None:
                                    safe_row[key] = ''
                                else:
                                    safe_row[key] = str(value)

                            # Skip rows with missing required fields
                            if PARAMETER_ANALYTE not in safe_row or not safe_row[PARAMETER_ANALYTE].strip():
                                logger.warning(f"Row {i} is missing required field {PARAMETER_ANALYTE}. Skipping.")
                                continue

                            processor.process_row(safe_row, i, lfile, filename, baddateonly, stopatdupvalue)
                        except Exception as e:
                            logger.error(f"Error processing row {i} with {encoding} encoding: {e}")
                            lfile.write(f"ERROR processing row {i} with {encoding} encoding: {e}\n")
                            continue
                break  # If we get here without exception, break the encoding loop
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.error(f"Error processing file with {encoding} encoding: {e}")
                continue
def main():
    """
    Entry point of the script.
    Sets up multiprocessing to handle multiple files concurrently,
    with a maximum number of processes, leaving 4 CPUs available.
    """
    directory = './2024/'
    multithread = True
    baddateonly = False
    stopatdupvalue = False

    # Calculate maximum processes, ensuring 4 CPUs remain available
    available_cpus = os.cpu_count() or 1
    reserved_cpus = 8
    max_processes = max(1, available_cpus - reserved_cpus)

    # Get list of all valid files first
    files_to_process = [
        filename for filename in os.listdir(directory)
        if filename.lower().endswith(('.xlsx', '.csv'))
    ]

    logger.info(f"Found {len(files_to_process)} files to process")
    logger.info(f"System has {available_cpus} CPUs, reserving {reserved_cpus}, using max {max_processes} processes")

    if multithread:
        # Process files in batches
        current_processes = []

        for filename in files_to_process:
            # Wait if we've reached the maximum number of processes
            while len(current_processes) >= max_processes:
                # Check each process and remove completed ones
                current_processes = [p for p in current_processes if p.is_alive()]
                time.sleep(0.1)  # Small delay to prevent CPU thrashing

            logger.info(f"Starting process for file: '{filename}'")
            p = Process(target=loadgrabdata, args=(directory, filename, baddateonly, stopatdupvalue))
            p.start()
            current_processes.append(p)

        # Wait for all remaining processes to complete
        for p in current_processes:
            p.join()
            logger.info(f"Process {p.pid} has completed")
    else:
        # Single-threaded processing
        for filename in files_to_process:
            logger.info(f"Processing file: '{filename}'")
            loadgrabdata(directory, filename, baddateonly, stopatdupvalue)

    logger.info("All files have been processed")


if __name__ == '__main__':
    # Add required import
    import time

    main()