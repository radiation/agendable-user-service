#!/bin/sh

echo "Adding services & routes to ${KONG_URL}..."

################
# User Service #
################

# Service
curl -i -X POST \
  --url ${KONG_URL}/services/ \
  --data 'name=user_service' \
  --data 'url=http://user_service:8004'

# Docs
curl -i -X POST \
  --url ${KONG_URL}/services/user_service/routes \
  --data 'name=user_service_docs' \
  --data 'paths[]=/user-service/docs' \
  --data 'strip_path=false'

# Other Routes
curl -i -X POST \
  --url ${KONG_URL}/services/user_service/routes \
  --data 'name=auth_route' \
  --data 'paths[]=/auth' \
  --data 'strip_path=false'

curl -i -X POST \
  --url ${KONG_URL}/services/user_service/routes \
  --data 'name=users_route' \
  --data 'paths[]=/users' \
  --data 'strip_path=false'

###################
# Meeting Service #
###################

# Service
curl -i -X POST \
  --url ${KONG_URL}/services/ \
  --data 'name=meeting_service' \
  --data 'url=http://meeting_service:8005' \
  --data "name=jwt"

# Docs
curl -i -X POST \
  --url ${KONG_URL}/services/meeting_service/routes \
  --data 'name=meeting_service_docs' \
  --data 'paths[]=/meeting-service/docs' \
  --data 'strip_path=false' \
  --data "name=jwt"

# Other Routes
curl -i -X POST \
  --url ${KONG_URL}/services/meeting_service/routes \
  --data 'name=meetings_route' \
  --data 'paths[]=/meetings' \
  --data 'strip_path=false' \
  --data "name=jwt"

curl -i -X POST \
  --url ${KONG_URL}/services/meeting_service/routes \
  --data 'name=recurrences_route' \
  --data 'paths[]=/meeting_recurrences' \
  --data 'strip_path=false' \
  --data "name=jwt"

curl -i -X POST \
  --url ${KONG_URL}/services/meeting_service/routes \
  --data 'name=attendees_route' \
  --data 'paths[]=/meeting_attendees' \
  --data 'strip_path=false' \
  --data "name=jwt"

curl -i -X POST \
  --url ${KONG_URL}/services/meeting_service/routes \
  --data 'name=tasks_route' \
  --data 'paths[]=/tasks' \
  --data 'strip_path=false' \
  --data "name=jwt"

curl -i -X POST \
  --url ${KONG_URL}/services/meeting_service/routes \
  --data 'name=meeting_tasks_route' \
  --data 'paths[]=/meeting_tasks' \
  --data 'strip_path=false' \
  --data "name=jwt"

# Enable JWT Plugin for Meeting Service
curl -i -X POST \
  --url ${KONG_URL}/services/meeting_service/plugins/ \
  --data "name=jwt" \
  --data "config.claims_to_verify=exp" \
  --data "config.key_claim_name=iss" \
  --data "config.secret_is_base64=false"

# Add a Consumer (e.g., meeting_service)
curl -i -X POST \
  --url ${KONG_URL}/consumers/ \
  --data "username=meeting_service_consumer"

# Associate a Public Key with the Consumer
curl -i -X POST \
  --url ${KONG_URL}/consumers/meeting_service_consumer/jwt/ \
  --data "key=your-issuer-claim" \
  --data "algorithm=HS256" \
  --data "secret=your-shared-secret"

curl -i -X POST \
  --url ${KONG_URL}/services/meeting_service/plugins/ \
  --data "name=request-transformer" \
  --data "config.add.headers=X-User-ID:\$claims.sub,X-User-Email:\$claims.email"
