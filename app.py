#!/usr/bin/env python3
import os

import aws_cdk as cdk
from dailymail.dailymail_stack import DailymailStack
import aws_cdk.cx_api

app = cdk.App()
DailymailStack(app, "DailymailStack")
app.synth()
