from langgraph.graph import StateGraph,END,START
import rigid_nodes_and_tools as nat
import agents

rigid_workflow = StateGraph(agents.RigidAgentState)

rigid_workflow.add_node('planner',nat.plan_node)
rigid_workflow.add_node('contacts',nat.contacts_node)
rigid_workflow.add_node('email',nat.email_node)

rigid_workflow.add_edge('planner','contacts')
rigid_workflow.add_edge('contacts','email')

rigid_workflow.set_entry_point('planner')
rigid_workflow.set_finish_point('email')

rigid_app = rigid_workflow.compile()

# Tests
rigid_app.invoke({'user':'Chase'})
rigid_app.invoke({'user':'Kyle'})
