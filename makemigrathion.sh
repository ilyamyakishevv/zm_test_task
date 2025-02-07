#!/usr/bin/env sh


alembic -c app/alembic.ini revision --autogenerate --message "$@"

