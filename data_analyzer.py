"""
This file contains the data analysis code initially. Please look at the other scripts for
the refined codes.
Analysis 1: Community Detection (Available in community_detection.py)
Analysis 2: Node Importance (Available in node_importance.py)
Analysis 3: Temporal analysis ( Available in data_visualaization_user_issued_currency.ipynb)
"""

import dbhelper
import networkx as nx
import matplotlib.pyplot as plt

session = dbhelper.getSession()
query = session.query(dbhelper.TransactionObject)
tesSUCCESS_list_BTC = query.filter(dbhelper.TransactionObject.amount_currency == 'BTC').all()
print("Total Number of successful BTC transactions: "+str(len(tesSUCCESS_list_BTC)))
tx_graph = nx.DiGraph()
c = ['r', 'g', 'b', 'k', 'c', 'm', 'y', 'w']
for tx in tesSUCCESS_list_BTC:
    accnt = tx.account
    dest = tx.destination
    _hash = tx.transaction_hash
    a_currency = tx.amount_currency
    d_currency = tx.delivered_currency

    if tx.transaction_result == 'tesSUCCESS':
        _color = c[0]
    elif tx.transaction_result == 'tecPATH_DRY':
        _color = c[1]
    elif tx.transaction_result == 'tecUNFUNDED_PAYMENT':
        _color = c[2]
    elif tx.transaction_result == 'tecNO_DST_INSUF_XRP':
        _color = c[3]
    elif tx.transaction_result == 'tecDST_TAG_NEEDED':
        _color = c[4]
    elif tx.transaction_result == 'tecPATH_PARTIAL':
        _color = c[5]
    elif tx.transaction_result == 'tecNO_DST':
        _color = c[6]
    elif tx.transaction_result == 'tecNO_PERMISSION':
        _color = c[7]

    tx_graph.add_edge(accnt, dest, hash=_hash, a_c=a_currency, d_c=d_currency, color=_color)

edges = tx_graph.edges()
nodes = tx_graph.nodes()
print('Number of Nodes: ', len(nodes), 'Number of edges: ', len(edges))
colors = [tx_graph[u][v]['color'] for u, v in edges]

print("Drawing Graph")
fig = plt.Figure(figsize=(15, 12), dpi=300)


_pos = nx.kamada_kawai_layout(tx_graph)
nx.draw_kamada_kawai( tx_graph, node_size=10, node_color='b', style='dotted', width=0.35, edge_color = colors)

plt.savefig('btc_success_tx_graph.jpg', dpi=300)
plt.show()
plt.close(fig)
session.close()
