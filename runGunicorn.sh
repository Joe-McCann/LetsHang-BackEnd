#!/bin/bash

cd /mnt/e/Bill/Documents/GitHubProjects/letsHang-BackEnd
source testing/bin/activate
gunicorn --reload letshang.app
