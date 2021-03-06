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

from sgsclient import base


class Replication(base.Resource):
    def __repr__(self):
        return "<Replication %s>" % self._info


class ReplicationManager(base.ManagerWithFind):
    resource_class = Replication

    def create(self, master_volume, slave_volume, name=None, description=None):
        body = {'replication': {'name': name,
                                'master_volume': master_volume,
                                'slave_volume': slave_volume,
                                'description': description
                                }}
        url = "/replications"
        return self._create(url, body, 'replication')

    def list(self, detailed=False, search_opts=None, marker=None, limit=None,
             sort_key=None, sort_dir=None, sort=None):
        """Lists all replications.

        :param detailed: Whether to return detailed volume info.
        :param search_opts: Search options to filter out replications.
        :param marker: Begin returning replications that appear later in the
                       replication list than that represented by this id.
        :param limit: Maximum number of replications to return.
        :param sort_key: Key to be sorted; deprecated in kilo
        :param sort_dir: Sort direction, should be 'desc' or 'asc'; deprecated
                         in kilo
        :param sort: Sort information
        :rtype: list of :class:`Replication`
        """
        resource_type = "replications"
        url = self._build_list_url(
            resource_type, detailed=detailed,
            search_opts=search_opts, marker=marker,
            limit=limit, sort_key=sort_key,
            sort_dir=sort_dir, sort=sort)
        return self._list(url, 'replications')

    def update(self, replication_id, **kwargs):
        if not kwargs:
            return
        body = {"replication": kwargs}
        return self._update('/replications/{replication_id}'
                            .format(replication_id=replication_id),
                            body, "replication")

    def delete(self, replication_id):
        path = '/replications/{replication_id}'.format(
            replication_id=replication_id)
        return self._delete(path)

    def get(self, replication_id, session_id=None):
        if session_id:
            headers = {'X-Configuration-Session': session_id}
        else:
            headers = {}
        url = "/replications/{replication_id}".format(
            replication_id=replication_id)
        return self._get(url, response_key="replication", headers=headers)

    def enable(self, replication_id):
        url = "/replications/{replication_id}/action".format(
            replication_id=replication_id)
        return self._action("enable", url, response_key='replication')

    def disable(self, replication_id):
        url = "/replications/{replication_id}/action".format(
            replication_id=replication_id)
        return self._action("disable", url, response_key='replication')

    def failover(self, replication_id, force=False):
        action_data = {'force': force}
        url = "/replications/{replication_id}/action".format(
            replication_id=replication_id)
        return self._action("failover", url, action_data,
                            response_key='replication')

    def reverse(self, replication_id):
        url = "/replications/{replication_id}/action".format(
            replication_id=replication_id)
        return self._action("reverse", url, response_key='replication')

    def reset_state(self, replication_id, state):
        action_data = {'status': state}
        url = "/replications/{replication_id}/action".format(
            replication_id=replication_id)
        return self._action('reset_status', url, action_data, 'replication')
