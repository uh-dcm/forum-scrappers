#!/bin/bash

set -euo pipefail

GIT_REPO_NAME=$(git remote get-url origin | awk -F'/' '{print $NF}' | sed 's/.git$//')
VENV_BASE="/home/${USER}/.venv"
VENV_PATH=${VENV_BASE}/${GIT_REPO_NAME}
DEPENDENCIES_FILE=$(git rev-parse --show-toplevel)/requirements.txt

mkdir -p ${VENV_BASE}

function usage() {
    echo "Usage: $0 create | activate | rm | recreate"
    echo ""
    echo "Options:"
    echo "  create    Create a new Python virtual environment."
    echo "  activate  Activate the existing Python virtual environment."
    echo "  rm        Remove the existing Python virtual environment."
    echo "  recreate  Recreate the Python virtual environment."
    echo ""
    exit 1
}

function create_venv() {
    if [ -d "${VENV_PATH}" ]; then
        echo "Virtual environment already exists at ${VENV_PATH}"
        usage
    fi
    python3 -m venv ${VENV_PATH}
    chmod +x ${VENV_PATH}/bin/activate
    echo "Virtual environment created at ${VENV_PATH}"
}

function activate_venv() {
    if ! [ -d "${VENV_PATH}" ]; then
        echo "Virtual environment does not exist at ${VENV_PATH}."
        usage
    fi
    if ! [ -f "${VENV_PATH}/bin/activate" ]; then
        echo "Activation file does not exist. Expected ${VENV_PATH}/bin/activate. Rerun with 'create'"
        usage
    fi
    source ${VENV_PATH}/bin/activate
    echo "Activated ${VENV_PATH}."
    echo "Installing dependencies... from ${DEPENDENCIES_FILE}"
    pip3 install -r ${DEPENDENCIES_FILE}
    echo ""
    echo "${GIT_REPO_NAME} venv ready!"
}

function rm_venv() {
    if [ -d "${VENV_PATH}" ]; then
        rm -rf "${VENV_PATH}"
        echo "Old virtual environment removed"
    fi
}

function recreate_venv() {
    rm_venv
    create
}

if [ $# -ne 1 ]; then
    usage
fi

case "${1}" in
    create)
        create_venv
        ;;
    activate)
        activate_venv
        ;;
    rm)
        rm_venv
        ;;
    recreate)
        recreate_venv
        ;;
    *)
        echo "Unknown option $1"
        usage
        ;;
esac



