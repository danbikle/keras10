#!/bin/bash

PGPASSWORD=ann psql -aP pager=no ann $@
exit
