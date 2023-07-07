#!/bin/bash
MANAGER="./tablelinker/manage.py"
TEMPLATES_DIR="tablelinker/dataset_templates/fixtures/standard_templates"

cd /app/

# Upgrade (migrate) database
echo "Migrating the database... "
${MANAGER} migrate

# Load fixtures
echo "Loading initial data... "
${MANAGER} loaddata --skip-checks users
${MANAGER} loaddata --skip-checks \
    ${TEMPLATES_DIR}/01_aed.yaml \
    ${TEMPLATES_DIR}/02_care_service.yaml \
    ${TEMPLATES_DIR}/03_hospital.yaml \
    ${TEMPLATES_DIR}/04_cultural_property.yaml \
    ${TEMPLATES_DIR}/05_tourism.yaml \
    ${TEMPLATES_DIR}/06_event.yaml \
    ${TEMPLATES_DIR}/07_public_wireless_lan.yaml \
    ${TEMPLATES_DIR}/08_public_toilet.yaml \
    ${TEMPLATES_DIR}/09_fire_hydrant.yaml \
    ${TEMPLATES_DIR}/10_evacuation_space.yaml \
    ${TEMPLATES_DIR}/11_population_yyyymmdd.yaml \
    ${TEMPLATES_DIR}/12_public_facility.yaml \
    ${TEMPLATES_DIR}/13_preschool.yaml \
    ${TEMPLATES_DIR}/14_open_data_list.yaml

# Download and install Jageocoder dictionary
JAGEOCODER_TRIE_FILE=${JAGEOCODER_DB_DIR}"/address.trie"
echo "Checking "${JAGEOCODER_TRIE_FILE}

if [ -f $JAGEOCODER_TRIE_FILE ]; then
    echo "Jageocoder dictionary has been installed."
else
    echo "Installing Jageocoder dictionary from the web... "
    python -m jageocoder install-dictionary
    echo "done."
fi

# Download and install Transformer model files
TRANSFORMER_MODEL_FILE=${TRANSFORMER_DIR}"/model/pytorch_model.bin"
echo "Checking "${TRANSFORMER_MODEL_FILE}

if [ -f $TRANSFORMER_MODEL_FILE ]; then
    echo "Transformer models has been installed."
else
    echo "Installing Transformer model files from the web... "
    python tablelinker/setup_transformer.py
    echo "done."
fi
