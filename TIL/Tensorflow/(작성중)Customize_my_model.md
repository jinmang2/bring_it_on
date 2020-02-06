# Customize My Model
자~ 오늘은 무엇을 해볼 거이냐!!!

우리 각자만의 모델을 `tensorflow`로 만들어보아요~ (와 씐난다!! 네 선생님!!!!)

지금은~ 퇴근 1시간 21분전!@!!! 의식의 흐름대로 작성해볼거니까~~~

잘 따라오셔야해요~~ 알겠쬬~?

네~~ 선떙님~~~

## `tf.estimator.Estimator`
- 일단 읽어라 노예야! [tf.estimator.Estimator](https://www.tensorflow.org/api_docs/python/tf/estimator/Estimator)
- `tf.compat.v1.estimator.Estimator`을 상속받음
```python
_VALID_MODEL_FN_ARGS = set(
    ['feature', 'labels', 'mode', 'params', 'self', 'config'])
# tensorflow.python.eager.monitoring
_estimator_api_gauge = monitoring.BoolGauge('/tensorflow/api/tensorflow',
                                            'estimator api usage', 'method')

@estimator_export(v1=['estimator.Estimator'])
class Estimator(object):
    def __init__(self,
                 model_fn,
                 mnodel_dir=None,
                 config=None,
                 params=None,
                 warm_start_from=None):
        _estimator_api_gauge.get_cell('init').set(True)
        # We do not endorse Estimator child classes to override methods in 
        # Estimator, other than a select few. You're on your own if you cleverly
        # override the method "_assert_members_are_not_overridden".
        self.__class__._assert_members_are_not_overridden(self) # pylint: disable=protected-access

        # 아래 코드 블럭의 함수로 override 체크
        self._config = maybe_overwrite_model_dir_and_session_config(config, model_dir)

        # The distribute field contains an instance of tf.distribute.Strategy.
        self._train_distribution = self._config.train_distribute
        self._eval_distribution = self._config.eval_distribute

        # Model directory
        self._model_dir = self._config.model_dir # model_dir을 Estimator객체에 저장
        self._session_config = self._config.session_config

        # logging config
        tf.compat.v1.logging.info('Using config: %s', str(vars(self._config)))

        self._device_fn = (
            self._config.device_fn or _get_replica_device_setter(self._config))
            
    ...
    def _assert_members_are_not_overridden(self):
        # Asserts members of `Estimator` are not overridden.
        _assert_members_are_not_overridden(Estimator, self)
```
```python
def _assert_members_are_not_overridden(cls, obj):
    """Assert Estimator methods are not overwritten."""
    # TPUEstimator is special cased (owned by TF).
    if obj.__class__.__name__ == 'TPUEstimator':
        return

def maybe_overwrite_model_dir_and_session_config(config, model_dir):
    # 덮어씌워질 수도 있으니 아래로 체크
    if config is None: # 없으면 default 사용
        config = run_config.RunConfig() # tensorflow_estimator.python.estimator.run_config
        tf.compat.v1.logging.info('Using default config.')
    if not isinstance(config, run_config.RunConfig): # RunConfig 객체가 아니면 오류 띄움
        raise ValueError(
            'config must be an instance of `RunConfig`, but provided %s.' % config)
    # config은 생기고 이 안에 session_config이 있는지 check
    if config.session_config is None: # 없으면
        session_config = run_config.get_default_session_config() # default 사용
        config = run_config.RunConfig.replace(config, session_config=session_config)

    model_dir = compat_internal.path_to_str(model_dir) # tensorflow.python.util.compat_internal
    if model_dir is not None: # model_dir이 None이 아니면
        if (getattr(config, 'model_dir', None) is not None and # config의 'model_dir' 속성이 None이 아닌데
            config.model_dir != model_dir):                    # arg의 model_dir과 다른 경우 에러 발생
            raise ValueError(
                "`model_dir` are set both in constructor and `RunConfig`, but with "
                "different values. In constructor: '{}', in `RunConfig`: "
                "'{}' ".format(model_dir, config.model_dir))
    if model_dir: # model_dir이 arg로 들어왔을 경우 config.model_dir = model_dir
        config = run_config.RunConfig.replace(config, model_dir=model_dir)
    elif getattr(config, 'model_dir', None) is None: # model_dir도 None, config.model_dir도 None이면
        model_dir = tempfile.mkdtemp() # 파이썬 임시파일을 만드는 내장 모듈
        tf.compat.v1.logging.warn('Using temporary folder as model directory: %s', model_dir) # 경고창 띄움
        config = run_config.RunConfig.replace(config, model_dir=model_dir) # 임시파일로 model_dir.

    return config
    
def _get_replica_device_setter(config):
    # 'device_fn'이 필요한 경우 가짜(replica) device setter를 생성
    if config.task_type:
        worker_device = '/job:%s/task:%d' % (config.task_type, config.task_id)
    else:
        worker_device = '/job:worker'
    
    if config.num_ps_replicas > 0:
        return tf.compat.v1.train.replica_device_setter(
            ps_tasks=config.num_ps_replicas,
            worker_device=worker_device,
            merge_devices=True,
            ps_ops=list(device_setter.STANDARD_PS_OPS),
            cluster=config.cluster_spec)
    else:
        return None
```
