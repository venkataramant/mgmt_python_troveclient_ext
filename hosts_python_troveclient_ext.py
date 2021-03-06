# Copyright 2011 OpenStack Foundation
# Copyright 2013 Rackspace Hosting
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from troveclient import base
from troveclient import common
from troveclient import utils


class Host(base.Resource):
    """
    A Hosts is an opaque instance used to store Host instances.
    """
    def __repr__(self):
        return "<Host: %s>" % self.name


class Hosts(base.ManagerWithFind):
    """
    Manage :class:`Host` resources.
    """
    resource_class = Host

    def _list(self, url, response_key):
        resp, body = self.api.client.get(url)
        if not body:
            raise Exception("Call to " + url + " did not return a body.")
        return [self.resource_class(self, res) for res in body[response_key]]

    def _action(self, host_id, body):
        """
        Perform a host "action" -- update
        """
        url = "/mgmt/hosts/%s/instances/action" % host_id
        resp, body = self.api.client.post(url, body=body)
        common.check_for_exceptions(resp, body, url)

    def update_all(self, host_id):
        """
        Update all instances on a host.
        """
        body = {'update': ''}
        self._action(host_id, body)

    def index(self):
        """
        List all hosts

        :rtype: list of :class:`Hosts`.
        """
        return self._list("/mgmt/hosts", "hosts")

    def get(self, host):
        """
        Show details of a host

        :rtype: :class:`host`
        """
        return self._get("/mgmt/hosts/%s" % self._get_host_name(host), "host")

    @staticmethod
    def _get_host_name(host):
        try:
            if host.name:
                return host.name
        except AttributeError:
            return host

    # Appease the abc gods
    def list(self):
        pass


@utils.service_type('database')
def do_mgmt_host_list(cs, args):
    """List all hosts"""
    hosts = cs.hosts_python_troveclient_ext.index()
    utils.print_list(hosts)


@utils.arg('host', metavar='<host>', help='Name of the host.')
@utils.service_type('database')
def do_mgmt_host_show(cs, args):
    """Show details of a host"""
    host = cs.hosts_python_troveclient_ext.get(args.host)
    utils.print_dict(host)


@utils.arg('host', metavar='<host>', help='ID of the host.')
@utils.service_type('database')
def do_mgmt_host_update_all(cs, args):
    """Update all instances on a host"""
    result = cs.hosts_python_troveclient_ext.update_all(args.host)
