#!/bin/bash
[[ -z "${PYTHON_APP}" ]] && { echo "PYTHON_APP required"; exit 1; }

cd /code
python ${PYTHON_APP}
