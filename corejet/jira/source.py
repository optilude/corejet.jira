from suds import WebFault
from suds.client import Client
from datetime import datetime

from corejet.core.model import RequirementsCatalogue, Epic, Story
from corejet.core.parser import appendScenarios

def jiraSource(details):
    """Produce a CoreJet XML file from JIRA. The parameter should be a
    comma-separated string with the following parameters:
    
    username=<username> - username to use to connect
    password=<password> - password to use to connect
    url=<url> - url of JIRA instance
    project=<name> - project name
    filter=<id> - id of filter that returns stories
    pointsField=<id> - id of field containing story points
    epicField=<id> - id of field indicating epic for a story
    acceptanceCriteriaField=<id> - id of field containing acceptance criteria
    """
    
    parameters = extractParameters(details)
    
    username = parameters['username']
    password = parameters['password']
    url = parameters['url']
    projectName = parameters['project']
    
    filterId = parameters['filter']
    pointsFieldId = parameters['pointsfield']
    epicFieldId = parameters['epicfield']
    acFieldId = parameters['acceptancecriteriafield']
    
    catalogue = RequirementsCatalogue(project=projectName, extractTime=datetime.now())
    
    # Open web service connection
    wsdl = url + "/rpc/soap/jirasoapservice-v2?wsdl"
    client = Client(wsdl)
    
    # Log into JIRA
    
    print "Fetching repository from JIRA instance at", url
    
    securityToken = client.service.login(username, password)
    
    epicCache = {}
    statuses = {}
    resolutions = {}
    
    try:
        
        # Look up statuses and resolutions
        
        for status in client.service.getStatuses(securityToken):
            statuses[status.id] = status.name
        
        for resolution in client.service.getResolutions(securityToken):
            resolutions[resolution.id] = resolution.name
        
        # Fetch all issues
        issues = client.service.getIssuesFromFilter(securityToken, filterId)
        
        for issue in issues:
            story = Story(issue.key, issue.summary)
            
            try:
                story.points = int(singleValueCustomFieldForIssue(issue, pointsFieldId))
            except (ValueError, TypeError):
                pass
            
            story.status = statuses.get(issue.status, None)
            story.resolution = resolutions.get(issue.resolution, None)
            
            epicName = singleValueCustomFieldForIssue(issue, epicFieldId)
            
            # See if this epic is a reference to an issue
            epic = epicCache.get(epicName, None)
            if epic is None:
                epicTitle = epicName
                try:
                    epicIssue = client.service.getIssue(securityToken, epicName)
                    epicTitle = epicIssue.summary
                except WebFault:
                    # Can't find the issue? We use the epic name as its title
                    pass
                
                # Create a new epic, cache it, and add it to the catalogue
                epicCache[epicName] = epic = Epic(epicName, epicTitle)
                catalogue.epics.append(epic)
            
            epic.stories.append(story)
            story.epic = epic
            
            acceptanceCriteria = singleValueCustomFieldForIssue(issue, acFieldId)
            try:
                appendScenarios(story, acceptanceCriteria)
            except ValueError, e:
                print "Error parsing acceptance criteria for", issue.key, "-", str(e)
    
    finally:
        client.service.logout(securityToken)
    
    return catalogue
    
def extractParameters(details):
    """Turn the parameters string into a dict
    """
    
    parameters = {}
    
    for option in details.split(','):
        key, value = option.split('=', 1)
        parameters[key.strip().lower()] = value.strip()
        
    return parameters

def customFieldForIssue(issue, fieldId):
    """Get the values of a custom field as a list
    """
    
    for fieldValue in issue.customFieldValues:
        customfieldId = fieldValue.customfieldId.replace("customfield_", "")
        if customfieldId == fieldId:
            return fieldValue.values

    return None

def singleValueCustomFieldForIssue(issue, fieldId):
    """Get a single value from a custom field
    """
    
    fieldMultiValues = customFieldForIssue(issue, fieldId)
    if not fieldMultiValues:
        return ""
    
    return fieldMultiValues[0]
