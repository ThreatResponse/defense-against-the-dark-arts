import boto3
import json

class CloudTrail(object):
    def __init__(self, trailArn):
        self.client = boto3.client('cloudtrail')
        self.arn = trailArn
        self.status = self.client.get_trail_status(
            Name=trailArn
        )

    """Check to see if Global Events are Active"""
    def globalEventsActive(self):
        if self.status[IncludeGlobalServiceEvents] == True:
            return True
        else:
            return False

    """Restart Logging on Trail ARN"""
    def EnableTrail(self):
        try:
            response = self.client.start_logging(
                Name=self.arn
            )
            return True
        except:
            return False

    """Check to see if CloudTrail is Logging"""
    def isLogging(self):
        if self.status['IsLogging']:
            return True
        else:
            return False

    """ Re-enable sending GlobalEvents to the Log"""
    def globalLogging(self):
        response = self.client.update_trail(
            Name=self.arn,
            IncludeGlobalServiceEvents=True
        )

"""
If CloudTrail is already enabled for all regions
do nothing otherwise restore CloudTrail to
a known good state based on a number of assumptions.
"""
def lambda_handler(event, context):
    print event
    """Strip trail Amazon ARN from Event"""
    trailArn = event['detail']['requestParameters']['name']

    """Instantiate CloudTrail Object"""
    c = CloudTrail(trailArn)

    """Enter an infinite loop waiting to return to known good state"""
    while c.isLogging() == False:
        c.EnableTrail()

    """Fix Global Event Logging"""
    if c.globalEventsActive() == False:
        c.globalLogging()
