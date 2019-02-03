import requests
import json
import os
import platform


class RpcClient:
    """JSON-RPC Client for VIPSTARCOIN"""

    def __init__(self, testnet=False, username=None, password=None,
                 ip='localhost', port=None, directory=None):

        if testnet:
            port = 32916
        elif port is None:
            port = 31916

        self.url = 'http://{0}:{1}'.format(ip, port)

        if username is None or password is None:
            if directory is None:
                self.username, self.password = self.__userpass()
            else:
                self.username, self.password = self.__userpass(_dir=directory)
        else:
            self.username = username
            self.password = password

        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.session.headers.update({'content-type': 'application/json'})

    @staticmethod
    def __userpass(_dir='VIPSTARCOIN'):
        """Reads config file for username/password"""

        username = None
        password = None

        os_name = platform.system()
        if os_name == 'Windows':
            source = os.path.expanduser('~/AppData/Roaming/{0}/{0}.conf').format(_dir)
        elif os_name == 'MacOS':
            source = os.path.expanduser('~/{0}/{0}.conf').format(_dir)
        else:
            print("error")

        dest = open(source, 'r')
        with dest as conf:
            for line in conf:
                if line.startswith('rpcuser'):
                    username = line.split("=")[1].strip()
                if line.startswith("rpcpassword"):
                    password = line.split("=")[1].strip()

        return username, password

    def req(self, method, params=()):
        """send request to VIPSTARCOINd"""

        data = json.dumps({"method": method, "params": params, "jsonrpc": "1.1"})

        try:
            response = self.session.post(self.url, data=data)
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(e.args)

        if response.status_code != requests.codes.ok:
            return dict(response.json()["error"])
        else:
            return response.json()["result"]

    def batch(self, reqs: list):
        """ send batch request using jsonrpc 2.0 """

        batch_data = []

        for req_id, req in enumerate(reqs):
            batch_data.append({"method": req[0], "params": req[1], "jsonrpc": "2.0", "id": req_id})

        data = json.dumps(batch_data)

        try:
            response = self.session.post(self.url, data=data).json()
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(e.args)

        return response

    ################################################################################
    # RPC methods
    # general syntax is req($method, [array_of_parameters])
    ################################################################################

    def fundrawtransaction(self, hexstring, options):
        """"""

        # TODO: untested
        return self.req("fundrawtransaction", [hexstring, options])

    def resendwallettransactions(self):
        """"""

        # TODO: untested
        return self.req("resendwallettransactions")

    def abandontransaction(self, txid):
        """"""

        # TODO: untested
        return self.req("abandontransaction", [txid])

    def addmultisigaddress(self, nrequired, keys, account=""):
        """"""

        # TODO: untested
        return self.req("addmultisigaddress", [nrequired, keys, account])

    def addwitnessaddress(self, address):
        """"""

        # TODO: untested
        return self.req("addwitnessaddress", [address])

    def backupwallet(self, destination="backup.dat"):
        """"""

        # TODO: untested
        return self.req("backupwallet", [destination])

    def bumpfee(self, txid, options=None):
        """"""

        # TODO: untested
        if options:
            return self.req("bumpfee", [txid, options])
        else:
            return self.req("bumpfee", [txid])

    def dumpprivkey(self, address):
        """returns privkey of address in WIF format."""

        return self.req("dumpprivkey", [address])

    def dumpwallet(self, filename):
        """"""

        # TODO: untested
        return self.req("dumpwallet", [filename])

    def encryptwallet(self, passphrase):
        """Encrypt wallet."""

        # TODO: untested
        return self.req("encryptwallet", [passphrase])

    def getaccountaddress(self, account=""):
        """get address associated with the <account>"""

        # TODO: untested
        return self.req("getaccountaddress", [account])

    def getaccount(self, address):
        """get account associated with <address>"""

        return self.req("getaccount", [address])

    def getaddressesbyaccount(self, account=""):
        """can be used to list asociated addresses"""

        return self.req("getaddressesbyaccount", [account])

    def getbalance(self, account=None, minconf=1, include_watchonly=False):
        """retrieve balance, If [account] is specified, returns the balance in the account."""

        if account:
            return self.req("getbalance", [account, minconf, include_watchonly])
        else:
            return self.req("getbalance")

    def getnewaddress(self, account=""):
        """return new address"""

        return self.req("getnewaddress", [account])

    def getrawchangeaddress(self):
        """"""

        # TODO: untested
        return self.req("getrawchangeaddress")

    def getreceivedbyaccount(self, account="", minconf=1):
        """"""

        # TODO: untested
        return self.req("getreceivedbyaccount", [account, minconf])

    def getreceivedbyaddress(self, address, minconf=1):
        """Returns the amount received by <address> in transactions
        with at least [minconf] confirmations."""

        # TODO: untested
        return self.req("getreceivedbyaddress", [address, minconf])

    def gettransaction(self, txid, include_watchonly=False, waitconf=0):
        """get transaction info"""

        # TODO: untested
        return self.req("gettransaction", [txid, include_watchonly, waitconf])

    def getunconfirmedbalance(self):
        """"""

        # TODO: untested
        return self.req("getunconfirmedbalance")

    def getwalletinfo(self):
        """"""

        # TODO: untested
        return self.req("getwalletinfo")

    def importmulti(self, requests, options='{ "rescan": true }'):
        """"""

        # TODO: untested
        return self.req("importmulti", [requests, options])

    def importprivkey(self, privkey, label="", rescan=True):
        """Import privatekey in WIF format"""

        # TODO: untested
        return self.req("importprivkey", [privkey, label, rescan])

    def importwallet(self, filename):
        """"""

        # TODO: untested
        return self.req("importwallet", [filename])

    def importaddress(self, address, label="", rescan=True, p2sh=False):
        """"""

        # TODO: untested
        return self.req("importaddress", [address, label, rescan, p2sh])

    def importprunedfunds(self, rawtransaction, txoutproof):
        """"""

        # TODO: untested
        return self.req("importprunedfunds", [rawtransaction, txoutproof])

    def importpubkey(self, pubkey, label="", rescan=True):
        """"""

        # TODO: untested
        return self.req("importpubkey", [pubkey, label, rescan])

    def keypoolrefill(self, newsize=100):
        """fils the keypoool"""

        # TODO: untested
        return self.req('keypoolrefill', [newsize])

    def listaccounts(self, minconf=1, include_watchonly=False):
        """list accounts in the wallet"""

        return self.req("listaccounts", [minconf, include_watchonly])

    def listaddressgroupings(self):
        """list accounts in the wallet"""

        # TODO: untested
        return self.req("listaddressgroupings")

    def listlockunspent(self):
        """Returns list of temporarily unspendable outputs."""

        # TODO: untested
        return self.req('listlockunspent')

    def listreceivedbyaccount(self, minconf=1, includeempty=False, include_watchonly=False):
        """list received by account"""

        # TODO: untested
        return self.req("listreceivedbyaccount", [minconf, includeempty, include_watchonly])

    def listreceivedbyaddress(self, minconf=1, includeempty=False, include_watchonly=False):
        """list received by account"""

        # TODO: untested
        return self.req("listreceivedbyaddress", [minconf, includeempty, include_watchonly])

    def listsinceblock(self, blockhash=None, target_confirmations=1, include_watchonly=False):
        """list received by account"""

        # TODO: untested
        if blockhash:
            return self.req("listsinceblock", [blockhash, target_confirmations, include_watchonly])
        else:
            return self.req("listsinceblock")

    def listtransactions(self, account="*", count=10, skip=0, include_watchonly=False):
        """list all transactions associated with this wallet"""

        # TODO: untested
        return self.req("listtransactions", [account, count, skip, include_watchonly])

    def listunspent(self, minconf=1, maxconf=9999999, addresses=None, include_unsafe=True):
        """list only unspent UTXO's"""

        # TODO: untested
        if addresses:
            return self.req("listunspent", [minconf, maxconf, addresses, include_unsafe])
        else:
            return self.req("listunspent", [minconf, maxconf])

    def lockunspent(self, unlock=None, transactions=None):
        """"""

        # TODO: untested
        if unlock is not None:
            return self.req('lockunspent', [unlock, transactions])
        else:
            return self.req('lockunspent')

    def move(self, fromaccount, toaccount, amount, minconf=1, comment=None):
        """"""

        if comment:
            return self.req("move", [fromaccount, toaccount, amount, minconf, comment])
        else:
            return self.req("move", [fromaccount, toaccount, amount])

    def reservebalance(self, reserve, amount):
        """Check if the reservebalance is specified."""

        # TODO: untested
        return self.req("reservebalance", [reserve, amount])

    def sendfrom(self, fromaccount, toaddress, amount, minconf=1, comment="", comment_to=""):
        """send outgoing tx from specified account to a given address"""

        # TODO: untested
        return self.req("sendfrom", [fromaccount, toaddress, amount, minconf, comment, comment_to])

    def sendmany(self, fromaccount, amounts="", minconf=1, comment="", subtractfeefrom=None):
        """send outgoing tx to many addresses, input is dict of addr:coins, returns txid"""

        # {"addr1":#coin,"addr2":#coin,"addr3":#coin...}
        # TODO: untested
        if subtractfeefrom:
            return self.req("sendmany", [fromaccount, amounts, minconf, comment, subtractfeefrom])
        else:
            return self.req("sendmany", [fromaccount, amounts, minconf, comment])

    def sendmanywithdupes(self, fromaccount, amounts="", minconf=1, comment="", subtractfeefrom=None):
        """"""

        # TODO: untested
        if subtractfeefrom:
            return self.req("sendmanywithdupes", [fromaccount, amounts, minconf, comment, subtractfeefrom])
        else:
            return self.req("sendmanywithdupes", [fromaccount, amounts, minconf, comment])

    def sendtoaddress(self, address, amount, comment="", comment_to="", subtractfeefromamount=False):
        """send ammount to address, with optional comment. Returns txid.
        sendtoaddress(ADDRESS, AMMOUNT, COMMENT)"""

        return self.req("sendtoaddress", [address, amount, comment, comment_to, subtractfeefromamount])

    def setaccount(self, address, account):
        """"""

        # TODO: untested
        return self.req("setaccount", [address, account])

    def settxfee(self, amount):
        """"""

        # TODO: untested
        return self.req("settxfee", [amount])

    def signmessage(self, address, message):
        """"""

        # TODO: untested
        return self.req("signmessage", [address, message])

    def walletlock(self):
        """"""

        return self.req("walletlock")

    def walletpassphrasechange(self, oldpassphrase, newpassphrase):
        """"""

        # TODO: untested
        return self.req("walletpassphrasechange", [oldpassphrase, newpassphrase])

    def walletpassphrase(self, passphrase, timeout, stakingonly):
        """"""

        return self.req("walletpassphrase", [passphrase, timeout, stakingonly])

    def removeprunedfunds(self, txid):
        """"""

        # TODO: untested
        return self.req("removeprunedfunds", [txid])

    def createcontract(self, bytecode, gasLimit, gasPrice, senderAddress, broadcast, changeToSender):
        """"""

        # TODO: untested
        return self.req("createcontract", [bytecode, gasLimit, gasPrice, senderAddress, broadcast, changeToSender])

    def sendtocontract(self, contractaddress, bytecode, amount, gasLimit, gasPrice, senderAddress, broadcast,
                       changeToSender):
        """"""

        # TODO: untested
        return self.req("sendtocontract",
                        [contractaddress, bytecode, amount, gasLimit, gasPrice, senderAddress, broadcast,
                         changeToSender])

    def help(self):
        """"""

        return self.req("help")

    def stop(self):
        """"""

        return self.req("stop")

    def getinfo(self):
        """"""

        return self.req("getinfo")

    def validateaddress(self, address):
        """"""

        return self.req("validateaddress", [address])
