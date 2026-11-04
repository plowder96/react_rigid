import model
import config
import agents
from typing import Type
import logger as l
import sample_db

CREDS = config.set_env()
LLM = model.model(CREDS['base'],CREDS['key'])
REL_CAND = model.relevant_candidate
STRUCTURED_MODEL = model.structured_model(REL_CAND,LLM)

# Deterministic driver for understanding if user message can be acted on as is.
def react_node(react_agent: Type[agents.ReactAgentState]):
    l.log_step('Running react_node')
    l.log_info(f'Checking entries exist for: {react_agent['user_name']}')

    matches = [name for name in sample_db.CONTACTS_DB.keys() if react_agent['user_name'].lower() in name.lower()]

    if len(matches) == 1:
        name = matches[0]
        l.log_info(f'Match found -> {name}')
        return {'details': {'name': name,**sample_db.CONTACTS_DB[name]},'flag': 'approve'}
    elif len(matches) > 1:
        l.log_warning(f'Ambiguity detected -> {matches}')
        return {'error': f'AMBIGUOUS; {matches}','flag': 'fail'}
    else:
        l.log_error('No contact found in DB.')
        return {'error': 'CONTACT_NOT_FOUND','flag': 'END'}

# Wired to an LLM for context inference when the contact provided is ambiguous(multiple returns from the DB).
def contact_node(react_agent: Type[agents.ReactAgentState]):
    l.log_step('Running contact_node (Retry Logic)')
    l.log_warning(f'Trying to resolve ambiguity....attempt #{react_agent['counter']}')

    candidate_fetch_prompt = f"""
        You are an expert in contextual reasoning.

        Your task is to analyze the provided user request and the empoloyee database. From the database, identify the single most relevant person to whom an email should be sent to accomplish the described task - even if multiple people have similar names or roles.

        Follow these principles:
        - Prioritize **exact or close matches** between the user's described role or department and the database entries.
        - Use contextual understanding - for instance, if the message asks 'Check the latest streamer new', prefer someone from the relevant department.
        - If multiple candidates are similar, choose the **most likely authoritative or contextually relevant** one.
        - Do **not** fabricate names or roles - only select from the given database.
        - Output should only contain the name and nothing else.
        ---

        ### TASK / USER MESSAGE:
        {react_agent['message']}

        ### EMPLOYEE DATABASE:
        {sample_db.CONTACTS_DB}

        ### SAMPLE OUTPUT:
        'John Carter'
        """

    react_agent['user_name'] = STRUCTURED_MODEL.invoke(candidate_fetch_prompt).user_name
    l.log_info(f'Selected most relevant candidate -> {react_agent['user_name']}')
    return react_agent

def retry_node(react_agent: Type[agents.ReactAgentState]):
    l.log_step('Running retry_node')
    l.log_info('No entry found for provided name, building response to the user for retry.')

    prompt = f"""
        You are an expert in contextual reasoning. Your task is to analyze the user request data and the employee database to determine if a typo exists in the user request.


    """

# Wired to an LLM for email generation based on provided user message.
def email_node(react_agent: Type[agents.ReactAgentState]):
    l.log_step('Running email_node')
    l.log_info(f'Sending email to: {react_agent['details'].get('email')}')

    prompt = f"""
        Write a professional email to {react_agent['details'].get('email')}.
        The topic of the email is {react_agent['message']}.
        Maintain a formal tone and provide a clear subject line and closing.
        Provide the following 3 pieces of the Email:

        **To:** <Email address of the recipient>
        **Subject:** <Subject of the email>
        **Body:** <Body of the email and closing>
        """

    react_agent['email_content'] = STRUCTURED_MODEL.invoke(prompt).content
    l.log_info(f'Email successfully generated with message:\n {react_agent['email_content']}')
    return react_agent

