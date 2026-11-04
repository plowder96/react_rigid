from langgraph.graph import StateGraph, END, START
import model
import agents
import config
import react_nodes

# TODO: Build the retry_node that searches for typos and responds to the user with relevant information.

react_workflow = StateGraph(agents.ReactAgentState)

react_workflow.add_node('react_node',react_nodes.react_node)
react_workflow.add_node('email_node',react_nodes.email_node)
react_workflow.add_node('contact_node',react_nodes.contact_node)

react_workflow.add_edge(START,'react_node')

# Conditional routing from react_node
react_workflow.add_conditional_edges(
    'react_node',
    lambda state: state['flag'],
    {
        'approve': 'email_node',
        'fail': 'contact_node',
        'END': END,
    }
)

# contact_node loops back to react_node
react_workflow.add_edge('contact_node','react_node')

# email ends workflow
react_workflow.add_edge('email_node',END)

react_app = react_workflow.compile()

# Tests
# Greenpath
react_app.invoke({'user_name': 'Chase','counter': 1, 'message': 'Please write an email to Chase asking how the latest changes to the DS department are going.'})

# Exception
# Name doesn't exist in the DB.
react_app.invoke({'user_name': 'Paul','counter': 1, 'message': 'Please write an email to Paul confirming our dinner reservations for this weekend.'})

# Name is ambiguous relative to DB data
react_app.invoke({'user_name': 'Kyle','counter': 1, 'message': 'Please write an email to Kyle confirming our dinner reservations for this weekend.'})

# Ambiguous name with better context in message
react_app.invoke({'user_name': 'Kyle','counter': 1, 'message': 'Please write an email to Kyle confirming that the streamer department is still having their monthly outing this month.'})
