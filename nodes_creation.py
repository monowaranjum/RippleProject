"""
This file populates the address nodes table of the ripple db.
Run this script after the loading of  transactions
"""

import dbhelper

session = dbhelper.getSession()
distinct_nodes = session.query(dbhelper.TransactionObject.account).distinct().all()
session.close()
print(len(distinct_nodes))
print((distinct_nodes[0][0]))

node_list = []

for item in distinct_nodes:
    node_list.append(dbhelper.AddressNode(address=item[0], incoming_nodes=0, outgoing_nodes=0))

dbhelper.add_addr_obj(node_list)
