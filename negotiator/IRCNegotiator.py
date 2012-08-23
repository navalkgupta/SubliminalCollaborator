# All of SubliminalCollaborator is licensed under the MIT license.

#   Copyright (c) 2012 Nick Lloyd

#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:

#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.

#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHE`R
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#   THE SOFTWARE.
from zope.interface import implements
from twisted.python import reactor, protocol, irc
import set


class IRCNegotiator(irc.IRCClient, protocol.ClientFactory):
    """
    IRC client implementation of the Negotiator interface.

    Negotiators are both protocols and factories for themselves.
    Not sure if this is the best way to do things but for now it
    will do.
    """
    implements(Negotiator)

    #*** irc.IRCClient properties ***#
    versionName = 'SubliminalCollaborator::IRCNegotiator'
    versionNum = 'pre-alpha'
    versionEnv = "Sublime Text 2"
    #******#

    clientConnection = None
    host = None
    port = None
    password = None

    peerUsers = None

    #*** Negotiator method implementations ***#

    def connect(host, port, username, password, **kwargs):
        """
        Connect to an instant messaging server.

        @param host: ip address or domain name of the host server
        @param port: C{int} port number of the host
        @param username: C{str} IM account username
        @param password: C{str} IM account password
        @param kwargs: {'channel': 'channelNameStringWoutPrefix'}

        @return: True on success
        """
        assert kwargs.has_key('channel')

        # start a fresh connection
        if self.clientConnection:
            self.clientConnection.disconnect()

        # irc.IRCClient member setting
        self.nickname = username

        self.host = host
        self.port = port
        self.password = password
        self.channel = kwargs['channel']
        self.peerUsers = []

        self.clientConnection = reactor.connectTCP(self.host, self.port, self)


    def isConnected():
        """
        Check if the connection is established and ready.

        @return: True on success, None if in-process, False on failure
        """
        if self.clientConnection and self._registered:
            return True
        elif self.clientConnection and not self._registered:
            return None
        else:
            return False
            

    def disconnect():
        """
        Disconnect from the instant messaging server.
        """
        if self.clientConnection:
            self.clientConnection.disconnect()


    def listUsers():
        """
        List the users available for establishing a peer-to-peer session.
        Depending on the implementing class this could either be a "friends list",
        the users within a certain chat room or channel, or
        a previously stored local list of known users.

        @return: C{Array} of usernames
        """
        pass

    def getUserName():
        """
        Return the final user nickname after connection to 
        the IRC server.

        @return: C{str} actual username
        """
        return self.nickname

    def negotiateSession(username):
        """
        Negotiate through the instant messaging layer a direct peer-to-peer connection
        with the user that has the given username.  Note the username in question must
        represent another SubliminalCollaborator Negotiator instance used by another
        user.

        If the user identified by the given username is not in the C{Array} returned
        by listUsers(), the expectation is that successful execution of this function
        will result in the given username being added to the list of known users.
        """
        pass

    def onNegotiateSession(username, host, port):
        """
        Callback method for incoming requests to start a peer-to-peer session.
        The username, host, and port of the requesting peer is provided as input.
        """
        pass

    #*** protocol.ClientFactory method implementations ***#

    def buildProtocol(self, addr):
        return self

    def clientConnectionLost(self, connector, reason):
        # may want to reconnect, but for now lets print why
        print 'connection lost: %s' % reason

    def clientConnectionFailed(self, connector, reason):
        print 'IRCNegotiator: connection failed: %s' % reason
