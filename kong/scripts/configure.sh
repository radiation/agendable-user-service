#!/bin/bash

echo "Adding services & routes to ${KONG_URL}..."

# Helper Functions
create_service() {
    local SERVICE_NAME=$1
    local SERVICE_URL=$2

    SERVICE_EXISTS=$(/usr/bin/curl -s ${KONG_URL}/services/$SERVICE_NAME | /usr/bin/jq -r '.name')
    if [ "$SERVICE_EXISTS" != "$SERVICE_NAME" ]; then
        echo "Creating $SERVICE_NAME..."
        /usr/bin/curl -i -X POST \
            --url ${KONG_URL}/services/ \
            --data "name=$SERVICE_NAME" \
            --data "url=$SERVICE_URL"
    else
        echo "Service $SERVICE_NAME already exists."
    fi
}

create_route() {
    local SERVICE_NAME=$1
    local ROUTE_NAME=$2
    local PATH=$3

    ROUTE_EXISTS=$(/usr/bin/curl -s ${KONG_URL}/routes/$ROUTE_NAME | /usr/bin/jq -r '.name')
    if [ "$ROUTE_EXISTS" != "$ROUTE_NAME" ]; then
        echo "Creating route $ROUTE_NAME..."
        /usr/bin/curl -i -X POST \
            --url ${KONG_URL}/services/$SERVICE_NAME/routes \
            --data "name=$ROUTE_NAME" \
            --data "paths[]=$PATH" \
            --data 'strip_path=false'
    else
        echo "Route $ROUTE_NAME already exists."
    fi
}

enable_plugin() {
    local SERVICE_NAME=$1
    local PLUGIN_NAME=$2
    shift 2
    local PLUGIN_CONFIG=$@

    PLUGIN_EXISTS=$(/usr/bin/curl -s ${KONG_URL}/services/$SERVICE_NAME/plugins | /usr/bin/jq -r ".data[] | select(.name==\"$PLUGIN_NAME\") | .name")
    if [ "$PLUGIN_EXISTS" != "$PLUGIN_NAME" ]; then
        echo "Enabling $PLUGIN_NAME Plugin for $SERVICE_NAME..."
        /usr/bin/curl -i -X POST \
            --url ${KONG_URL}/services/$SERVICE_NAME/plugins/ \
            --data "name=$PLUGIN_NAME" $PLUGIN_CONFIG
    else
        echo "$PLUGIN_NAME Plugin already enabled for $SERVICE_NAME."
    fi
}

create_consumer() {
    local CONSUMER_NAME=$1

    CONSUMER_EXISTS=$(/usr/bin/curl -s ${KONG_URL}/consumers/$CONSUMER_NAME | /usr/bin/jq -r '.username')
    if [ "$CONSUMER_EXISTS" != "$CONSUMER_NAME" ]; then
        echo "Creating consumer $CONSUMER_NAME..."
        /usr/bin/curl -i -X POST \
            --url ${KONG_URL}/consumers/ \
            --data "username=$CONSUMER_NAME"
    else
        echo "Consumer $CONSUMER_NAME already exists."
    fi
}

associate_jwt() {
    local CONSUMER_NAME=$1
    local JWT_KEY=$2
    local JWT_SECRET=$3

    JWT_EXISTS=$(/usr/bin/curl -s ${KONG_URL}/consumers/$CONSUMER_NAME/jwt | /usr/bin/jq -r ".data[] | select(.key==\"$JWT_KEY\") | .key")
    if [ "$JWT_EXISTS" != "$JWT_KEY" ]; then
        echo "Associating JWT with consumer $CONSUMER_NAME..."
        /usr/bin/curl -i -X POST \
            --url ${KONG_URL}/consumers/$CONSUMER_NAME/jwt/ \
            --data "key=$JWT_KEY" \
            --data "algorithm=HS256" \
            --data "secret=$JWT_SECRET"
    else
        echo "JWT already associated with $CONSUMER_NAME."
    fi
}

# Main Script
# Create Services
create_service "user-service" "http://user-service:8004"
create_service "meeting-service" "http://meeting-service:8005"

# Create Routes for User Service
USER_ROUTES=("user_service_docs:/docs" "auth_route:/auth" "users_route:/users" \
             "roles_route:/roles" "groups_route:/groups" "openapi_json:/openapi.json")
for ROUTE in "${USER_ROUTES[@]}"; do
    NAME=$(echo "$ROUTE" | /usr/bin/cut -d':' -f1)
    PATH=$(echo "$ROUTE" | /usr/bin/cut -d':' -f2)
    create_route "user-service" "$NAME" "$PATH"
done

# Create Routes for Meeting Service
MEETING_ROUTES=("meeting_service_docs:/docs" "meetings_route:/meetings" \
                "recurrences_route:/meeting_recurrences" "attendees_route:/meeting_attendees" \
                "tasks_route:/tasks" "meeting_tasks_route:/meeting_tasks" \
                "openapi_json:/openapi.json" "meeting_users_route:/meeting_users")
for ROUTE in "${MEETING_ROUTES[@]}"; do
    NAME=$(echo "$ROUTE" | /usr/bin/cut -d':' -f1)
    PATH=$(echo "$ROUTE" | /usr/bin/cut -d':' -f2)
    create_route "meeting-service" "$NAME" "$PATH"
done

# Enable Plugins
enable_plugin "meeting-service" "jwt" \
    --data "config.claims_to_verify=exp" \
    --data "config.key_claim_name=iss" \
    --data "config.secret_is_base64=false"

enable_plugin "meeting-service" "request-transformer" \
    --data "config.add.headers=X-User-ID:\$claims.sub" \
    --data "config.add.headers=X-User-Email:\$claims.email"

enable_plugin "meeting-service" "cors" \
    --data "config.origins=*" \
    --data "config.methods[]=GET" \
    --data "config.methods[]=HEAD" \
    --data "config.methods[]=PUT" \
    --data "config.methods[]=PATCH" \
    --data "config.methods[]=POST" \
    --data "config.methods[]=DELETE" \
    --data "config.methods[]=OPTIONS" \
    --data "config.headers[]=Content-Type" \
    --data "config.headers[]=Authorization" \
    --data "config.exposed_headers[]=Authorization" \
    --data "config.credentials=true"

enable_plugin "user-service" "cors" \
    --data "config.origins=*" \
    --data "config.methods[]=GET" \
    --data "config.methods[]=HEAD" \
    --data "config.methods[]=PUT" \
    --data "config.methods[]=PATCH" \
    --data "config.methods[]=POST" \
    --data "config.methods[]=DELETE" \
    --data "config.methods[]=OPTIONS" \
    --data "config.headers[]=Content-Type" \
    --data "config.headers[]=Authorization" \
    --data "config.exposed_headers[]=Authorization" \
    --data "config.credentials=true"

# Create Consumer and Associate JWT
create_consumer "user-service-consumer"
associate_jwt "user-service-consumer" "user-service" "$SECRET_KEY"
