#!/usr/bin/env python3
import os

import aws_cdk as cdk
from dailymail.dailymail_stack import DailymailStack


app = cdk.App()
DailymailStack(app, "DailymailStack")
app.synth()
