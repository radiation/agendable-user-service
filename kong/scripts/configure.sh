#!/bin/bash

echo "Adding services & routes to ${KONG_URL}..."

################
# User Service #
################

# Check if the User Service exists
SERVICE_EXISTS=$(/usr/bin/curl -s ${KONG_URL}/services/user_service | /usr/bin/jq -r '.name')
if [ "$SERVICE_EXISTS" != "user_service" ]; then
    echo "Creating user_service..."
    /usr/bin/curl -i -X POST \
        --url ${KONG_URL}/services/ \
        --data 'name=user_service' \
        --data 'url=http://user_service:8004'
else
    echo "Service user_service already exists."
fi

# Check and create routes for the User Service
ROUTES=("user_service_docs:/user-service/docs" "auth_route:/auth" "users_route:/users")
for ROUTE in "${ROUTES[@]}"; do
    NAME=$(echo "$ROUTE" | /usr/bin/cut -d':' -f1)
    PATH=$(echo "$ROUTE" | /usr/bin/cut -d':' -f2)

    ROUTE_EXISTS=$(/usr/bin/curl -s ${KONG_URL}/routes/$NAME | /usr/bin/jq -r '.name')
    if [ "$ROUTE_EXISTS" != "$NAME" ]; then
        echo "Creating route $NAME..."
        /usr/bin/curl -i -X POST \
            --url ${KONG_URL}/services/user_service/routes \
            --data "name=$NAME" \
            --data "paths[]=$PATH" \
            --data 'strip_path=false'
    else
        echo "Route $NAME already exists."
    fi
done

###################
# Meeting Service #
###################

# Check if the Meeting Service exists
SERVICE_EXISTS=$(/usr/bin/curl -s ${KONG_URL}/services/meeting_service | /usr/bin/jq -r '.name')
if [ "$SERVICE_EXISTS" != "meeting_service" ]; then
    echo "Creating meeting_service..."
    /usr/bin/curl -i -X POST \
        --url ${KONG_URL}/services/ \
        --data 'name=meeting_service' \
        --data 'url=http://meeting_service:8005'
else
    echo "Service meeting_service already exists."
fi

# Check and create routes for the Meeting Service
ROUTES=("meeting_service_docs:/meeting-service/docs" "meetings_route:/meetings" \
        "recurrences_route:/meeting_recurrences" "attendees_route:/meeting_attendees" \
        "tasks_route:/tasks" "meeting_tasks_route:/meeting_tasks")
for ROUTE in "${ROUTES[@]}"; do
    NAME=$(echo "$ROUTE" | /usr/bin/cut -d':' -f1)
    PATH=$(echo "$ROUTE" | /usr/bin/cut -d':' -f2)

    ROUTE_EXISTS=$(/usr/bin/curl -s ${KONG_URL}/routes/$NAME | /usr/bin/jq -r '.name')
    if [ "$ROUTE_EXISTS" != "$NAME" ]; then
        echo "Creating route $NAME..."
        /usr/bin/curl -i -X POST \
            --url ${KONG_URL}/services/meeting_service/routes \
            --data "name=$NAME" \
            --data "paths[]=$PATH" \
            --data 'strip_path=false'
    else
        echo "Route $NAME already exists."
    fi
done

# Enable JWT Plugin for Meeting Service
PLUGIN_EXISTS=$(/usr/bin/curl -s ${KONG_URL}/services/meeting_service/plugins | /usr/bin/jq -r '.data[] | select(.name=="jwt") | .name')
if [ "$PLUGIN_EXISTS" != "jwt" ]; then
    echo "Enabling JWT Plugin for meeting_service..."
    /usr/bin/curl -i -X POST \
        --url ${KONG_URL}/services/meeting_service/plugins/ \
        --data "name=jwt" \
        --data "config.claims_to_verify=exp" \
        --data "config.key_claim_name=iss" \
        --data "config.secret_is_base64=false"
else
    echo "JWT Plugin already enabled for meeting_service."
fi

# Check and add a Consumer
CONSUMER_EXISTS=$(/usr/bin/curl -s ${KONG_URL}/consumers/user-service-consumer | /usr/bin/jq -r '.username')
if [ "$CONSUMER_EXISTS" != "user-service-consumer" ]; then
    echo "Creating consumer user-service-consumer..."
    /usr/bin/curl -i -X POST \
        --url ${KONG_URL}/consumers/ \
        --data "username=user-service-consumer"
else
    echo "Consumer user-service-consumer already exists."
fi

# Check and associate JWT with the Consumer
JWT_EXISTS=$(/usr/bin/curl -s ${KONG_URL}/consumers/user-service-consumer/jwt | /usr/bin/jq -r '.data[] | select(.key=="user-service") | .key')
if [ "$JWT_EXISTS" != "user-service" ]; then
    echo "Associating JWT with consumer user-service-consumer..."
    /usr/bin/curl -i -X POST \
        --url ${KONG_URL}/consumers/user-service-consumer/jwt/ \
        --data "key=user-service" \
        --data "algorithm=HS256" \
        --data "secret=${SECRET_KEY}"
else
    echo "JWT already associated with user-service-consumer."
fi

# Enable request-transformer Plugin for Meeting Service
PLUGIN_EXISTS=$(/usr/bin/curl -s ${KONG_URL}/services/meeting_service/plugins | /usr/bin/jq -r '.data[] | select(.name=="request-transformer") | .name')
if [ "$PLUGIN_EXISTS" != "request-transformer" ]; then
    echo "Enabling request-transformer Plugin for meeting_service..."
    /usr/bin/curl -i -X POST \
        --url ${KONG_URL}/services/meeting_service/plugins/ \
        --data "name=request-transformer" \
        --data "config.add.headers=X-User-ID:\\$claims.sub,X-User-Email:\\$claims.email"
else
    echo "request-transformer Plugin already enabled for meeting_service."
fi
