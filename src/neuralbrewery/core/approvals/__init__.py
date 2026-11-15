"""The queue of approvals as the rest of the app sees it.

- schemas.py: who acts on a proposal (Actor), what a proposer gets back
  (Receipt), what the agent recalls of a past proposal (PastDecision);
  plain Python
- protocols.py: ProposalInbox, the one way an agent or the MCP server puts
  a proposal in the queue; DecisionReader, the one way the plant agent
  reads what the brewer decided on its proposals

features/approvals implements both, bootstrap.py hands each to who needs
it. Approving is in neither: an agent can only propose and recall.
"""
