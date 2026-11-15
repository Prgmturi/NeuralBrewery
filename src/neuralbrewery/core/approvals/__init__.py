"""The queue of approvals as the rest of the app sees it: a box for proposals.

- schemas.py: who acts on a proposal (Actor), what a proposer gets back
  (Receipt); plain Python
- protocols.py: ProposalInbox, the one way an agent or the MCP server puts
  a proposal in the queue

features/approvals implements the port, bootstrap.py hands it to who may
propose. Approving is not in the port: an agent can only propose.
"""
