# Copyright 2024 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


def v3io_cred(api="", user="", access_key=""):
    """
    Modifier function to copy local v3io env vars to container

    Usage::

        train = train_op(...)
        train.apply(use_v3io_cred())
    """
    raise NotImplementedError


def mount_v3io(
    name="v3io",
    remote="",
    access_key="",
    user="",
    secret=None,
    volume_mounts=None,
):
    """Modifier function to apply to a Container Op to volume mount a v3io path

    :param name:            the volume name
    :param remote:          the v3io path to use for the volume. ~/ prefix will be replaced with /users/<username>/
    :param access_key:      the access key used to auth against v3io. if not given V3IO_ACCESS_KEY env var will be used
    :param user:            the username used to auth against v3io. if not given V3IO_USERNAME env var will be used
    :param secret:          k8s secret name which would be used to get the username and access key to auth against v3io.
    :param volume_mounts:   list of VolumeMount. empty volume mounts & remote will default to mount /v3io & /User.
    """
    raise NotImplementedError


def mount_v3iod(namespace, v3io_config_configmap):
    raise NotImplementedError


def mount_pvc(pvc_name=None, volume_name="pipeline", volume_mount_path="/mnt/pipeline"):
    """
    Modifier function to apply to a Container Op to simplify volume, volume mount addition and
    enable better reuse of volumes, volume claims across container ops.

    Usage::

        train = train_op(...)
        train.apply(mount_pvc('claim-name', 'pipeline', '/mnt/pipeline'))
    """
    raise NotImplementedError


def set_env_variables(env_vars_dict: dict[str, str] = None, **kwargs):
    """
    Modifier function to apply a set of environment variables to a runtime. Variables may be passed
    as either a dictionary of name-value pairs, or as arguments to the function.
    See `KubeResource.apply` for more information on modifiers.

    Usage::

        function.apply(set_env_variables({"ENV1": "value1", "ENV2": "value2"}))
        or
        function.apply(set_env_variables(ENV1=value1, ENV2=value2))

    :param env_vars_dict: dictionary of env. variables
    :param kwargs: environment variables passed as args
    """
    raise NotImplementedError


def mount_s3(
    secret_name=None,
    aws_access_key="",
    aws_secret_key="",
    endpoint_url=None,
    prefix="",
    aws_region=None,
    non_anonymous=False,
):
    """Modifier function to add s3 env vars or secrets to container

    **Warning:**
    Using this function to configure AWS credentials will expose these credentials in the pod spec of the runtime
    created. It is recommended to use the `secret_name` parameter, or set the credentials as project-secrets and avoid
    using this function.

    :param secret_name: kubernetes secret name (storing the access/secret keys)
    :param aws_access_key: AWS_ACCESS_KEY_ID value. If this parameter is not specified and AWS_ACCESS_KEY_ID env.
                            variable is defined, the value will be taken from the env. variable
    :param aws_secret_key: AWS_SECRET_ACCESS_KEY value. If this parameter is not specified and AWS_SECRET_ACCESS_KEY
                            env. variable is defined, the value will be taken from the env. variable
    :param endpoint_url: s3 endpoint address (for non AWS s3)
    :param prefix: string prefix to add before the env var name (for working with multiple s3 data stores)
    :param aws_region: amazon region
    :param non_anonymous: force the S3 API to use non-anonymous connection, even if no credentials are provided
        (for authenticating externally, such as through IAM instance-roles)
    """
    raise NotImplementedError


def mount_spark_conf():
    raise NotImplementedError


def mount_secret(secret_name, mount_path, volume_name="secret", items=None):
    """Modifier function to mount kubernetes secret as files(s)

    :param secret_name:  k8s secret name
    :param mount_path:   path to mount inside the container
    :param volume_name:  unique volume name
    :param items:        If unspecified, each key-value pair in the Data field
                         of the referenced Secret will be projected into the
                         volume as a file whose name is the key and content is
                         the value.
                         If specified, the listed keys will be projected into
                         the specified paths, and unlisted keys will not be
                         present.
    """
    raise NotImplementedError


def mount_configmap(configmap_name, mount_path, volume_name="configmap", items=None):
    """Modifier function to mount kubernetes configmap as files(s)

    :param configmap_name:  k8s configmap name
    :param mount_path:      path to mount inside the container
    :param volume_name:     unique volume name
    :param items:           If unspecified, each key-value pair in the Data field
                            of the referenced Configmap will be projected into the
                            volume as a file whose name is the key and content is
                            the value.
                            If specified, the listed keys will be projected into
                            the specified paths, and unlisted keys will not be
                            present.
    """
    raise NotImplementedError


def mount_hostpath(host_path, mount_path, volume_name="hostpath"):
    """Modifier function to mount kubernetes configmap as files(s)

    :param host_path:  host path
    :param mount_path:   path to mount inside the container
    :param volume_name:  unique volume name
    """
    raise NotImplementedError


def auto_mount(pvc_name="", volume_mount_path="", volume_name=None):
    """choose the mount based on env variables and params

    volume will be selected by the following order:
    - k8s PVC volume when both pvc_name and volume_mount_path are set
    - k8s PVC volume when env var is set: MLRUN_PVC_MOUNT=<pvc-name>:<mount-path>
    - k8s PVC volume if it's configured as the auto mount type
    - iguazio v3io volume when V3IO_ACCESS_KEY and V3IO_USERNAME env vars are set
    """
    raise NotImplementedError
