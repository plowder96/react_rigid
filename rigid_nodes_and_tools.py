import sample_db
import agents
import logger as l
from typing import Type

# Plan node for the rigid agent is predetermined:
#   Step 1 - Get the contact name for the 'user'
#   Step 2 - Send the email to the 'user'
def plan_node(rigid_agent: Type[agents.RigidAgentState]):
    l.log_step('Running plan_node')

    l.log_info(f'Planning next actions based on user request -> \'{rigid_agent['user']}\'')

    plan = {
        'steps': [
            ('contacts',rigid_agent['user']),
            ('email_send',rigid_agent['user'])
        ]
    }

    l.log_info(f'Generated execution plan -> {plan['steps']}')
    return plan

def contacts_tool(query_name:str):
    """Return a single contact or an ambiguous results with logs."""
    l.log_step('Running contacts_tool')
    l.log_info(f'Searching DB for: \'{query_name}\'')

    matches = [name for name in sample_db.CONTACTS_DB.keys() if query_name.lower() in name.lower()]

    if len(matches) == 1:
        name = matches[0]
        l.log_info(f'Match found -> \'{name}\'')
        return {'success': True,'contact': {'name':name,**sample_db.CONTACTS_DB[name]}}
    elif len(matches) > 1:
        l.log_warning(f'Multiple matches found {matches}')
        return {'success': False,'error': f'AMBIGUOUS: {matches}'}
    else:
        l.log_error('No matching name in DB')
        return {'success': False,'error': 'CONTACT_NOT_FOUND'}

# The contacts node checks the DB for the contact.
#   Calls contacts_tool for direct, ambiguous, or no match
def contacts_node(rigid_agent: Type[agents.RigidAgentState]):
    l.log_step('Running contacts_node')

    step_action,step_arg = rigid_agent['steps'][0]
    l.log_info(f'Step action: {step_action} | Looking for contact: {step_arg}')

    result = contacts_tool(step_arg)

    l.log_info(f'Saving result to state -> {result}')

    rigid_agent['contact_result'] = result
    return rigid_agent

def email_send_tool(contact: dict,subject: str,body: str):
    """Simulate sending an email."""
    l.log_info(f'Sending email to {contact['name']} ({contact['email']})')

    return f'Email sent to {contact['name']} ({contact['email']}) | subject=\'{subject}\''

# The email node takes the contact node results and forms and email if contact search was successful.
def email_node(rigid_agent: Type[agents.RigidAgentState]):
    l.log_step('Running email_node')

    result = rigid_agent['contact_result']
    l.log_info(f'Previous step result -> {result}')

    if not result['success']:
        error_msg = f'Cannot send email: {result['error']}'
        l.log_error(error_msg)
        rigid_agent['email_result'] = error_msg
        return rigid_agent

    contact = result['contact']
    l.log_info(f'Resolved contact -> {contact['name']} ({contact['email']})')
    
    # sample email subject/body
    subject = 'Test subject'
    body = 'test body'

    l.log_info(f'Preparing email...\nSubject: {subject}\nBody: {body}')

    final = email_send_tool(contact,subject,body)

    l.log_info(f'Email operation completed successffully.')
    rigid_agent['email_result'] = final

    return rigid_agent
