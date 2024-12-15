#!/bin/bash - 
#===============================================================================
#
#          FILE: sync-rdf-with-showvoc.sh
# 
#         USAGE: ./sync-rdf-with-showvoc.sh
# 
#   DESCRIPTION: Loads remote RDF data into a ShowVoc (Semantic Turkey) project.
# 
#        AUTHOR: Nicolas Broussard (nicolas@togetherfor.it)
#  ORGANIZATION: Together for it
#       CREATED: 11/30/2024 11:44:17 CET
#===============================================================================

set -euo pipefail                                  # https://bit.ly/eouxpipefail

function login() {
  # Ask password, if not provided
  if [ -z "$USER_PASSWORD" ]; then
    read -rsp "Password for $USER_EMAIL: " USER_PASSWORD
  fi
  LOGIN_RESPONSE=$(
    curl -s -D - "${ST_ENDPOINT%/}/Auth/login" \
      -F "email=${USER_EMAIL}" \
      -F "password=${USER_PASSWORD}" \
      -F "_spring_security_remember_me=false" \
      --insecure
  )
  SESSION_TOKEN=$(echo "$LOGIN_RESPONSE" | sed -n 's/set-cookie: JSESSIONID=\([^;]*\).*/\1/p')
  echo $SESSION_TOKEN
}

function sync() {
  SYNC_RESPONSE=$(
    curl -s "${ST_ENDPOINT%/}/InputOutput/loadRDF?ctx_project=${PROJECT_NAME}" \
      -H "Cookie: JSESSIONID=${SESSION_TOKEN}" \
      -F "baseURI=${BASE_URI}" \
      -F "transitiveImportAllowance=${TRANSITIVE_IMPORT_ALLOWANCE}" \
      -F "format=${FORMAT}" \
      -F "loaderSpec=${LOADER_SPEC}" \
      -F "rdfLifterSpec=${RDF_LIFTER_SPEC}" \
      -F "transformationPipeline=${TRANSFORMATION_PIPELINE}" \
      --insecure
  )
  echo $SYNC_RESPONSE
}

# Validate required inputs

SHOWVOC_URL=${SHOWVOC_URL:-}
PROJECT_NAME=${PROJECT_NAME:-}
RDF_FILE_URL=${RDF_FILE_URL:-}
RDF_BASE_URI=${RDF_BASE_URI:-}
USER_EMAIL=${USER_EMAIL:-}
USER_PASSWORD=${USER_PASSWORD:-}

if [[ -z "$SHOWVOC_URL"  || -z "$PROJECT_NAME" || -z "$RDF_FILE_URL" ||
      -z "$RDF_BASE_URI" || -z "$USER_EMAIL"                            ]]; then
  echo "Error: Missing required environment variables." >&2
  echo "Ensure the following are set: SHOWVOC_URL, USER_EMAIL, PROJECT_NAME, RDF_FILE_URL, RDF_BASE_URI." >&2
  echo "Optional: USER_PASSWORD will be prompted if not set." >&2
  exit 1
fi

# Prepare request parameters

ST_ENDPOINT="${SHOWVOC_URL%/}/semanticturkey/it.uniroma2.art.semanticturkey/st-core-services"
BASE_URI="${RDF_BASE_URI}"
TRANSITIVE_IMPORT_ALLOWANCE='web'
FORMAT='RDF/XML'
LOADER_SPEC=$(cat <<EOF
{
  "factoryId": "it.uniroma2.art.semanticturkey.extension.impl.loader.http.HTTPLoader",
  "configType": "it.uniroma2.art.semanticturkey.extension.impl.loader.http.HTTPLoaderConfiguration",
  "configuration": {
    "@type": "it.uniroma2.art.semanticturkey.extension.impl.loader.http.HTTPLoaderConfiguration",
    "endpoint": "${RDF_FILE_URL}",
    "enableContentNegotiation": true,
    "reportContentType": false
  }
}
EOF
)
RDF_LIFTER_SPEC='{
  "factoryId": "it.uniroma2.art.semanticturkey.extension.impl.rdflifter.rdfdeserializer.RDFDeserializingLifter"
}'
TRANSFORMATION_PIPELINE='[]'

# Log in

echo "Logging in to ShowVoc..."
SESSION_TOKEN=$(login)

if [[ -z "$SESSION_TOKEN" ]]; then
  echo "Error: Login failed. Unable to retrieve session token." >&2
  exit 1
fi
echo "Login successful."

# Synchronize

echo "Syncing RDF to ShowVoc..."
echo
echo "Source: ${RDF_FILE_URL}"
echo "Base URI: ${BASE_URI}"
echo "Destination project: ${PROJECT_NAME}"
echo
SYNC_RESPONSE=$(sync)
RESPONSE_TYPE=$(echo ${SYNC_RESPONSE} | jq -r '.stresponse.type')

if [[ "${RESPONSE_TYPE}" == 'error' || "${RESPONSE_TYPE}" == 'exception' ]]; then
  STACK_TRACE=$(echo ${SYNC_RESPONSE} | jq -r '.stresponse.stackTrace')
  echo "Stack trace: " >&2
  echo -e "${STACK_TRACE}\n" >&2
  echo "RDF sync failed." >&2
  exit 1
fi

echo "🍺 RDF sync completed successfully."
exit 0
