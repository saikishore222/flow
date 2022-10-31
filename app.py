from dotenv import dotenv_values
from gql import gql, Client
from flask import Flask,jsonify
from gql.transport.aiohttp import AIOHTTPTransport
env = dotenv_values()
headers = {"Authorization": f"Bearer {env['DEST_TOKEN']}"}
transport = AIOHTTPTransport(url=env['DEST_URL'], headers=headers)
client = Client(transport=transport)
app = Flask(__name__)
@app.route('/account/<id>', methods=['GET'])
def Account(id):
    print(type(id))
    print(id)
    query=gql("""
    query AccountTransactions {
  account(id: "%s") {
    address
    balance
    domainNames {
      name
      fullName
      provider
    }
    contracts {
      id
      address
    }
    transactions (
      first: 5
      ordering: Descending
    ) {
      edges {
        cursor
        node {
          hash
          height
          index
          status
          sequenceNumber
          eventCount
          proposer {
            address
          }
          payer {
            address
          }
          authorizers {
            address
          }
        }
      }
    }
  }
    }
 """%(id)
    )
    response = client.execute(query)
    return jsonify(response)
app.run()