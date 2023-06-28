#!/bin/bash

if [ "$DEBUG_MODE" = "True" ] ; then
    python frontend.py
else
    exec gunicorn -b :8050 frontend:server
fi
