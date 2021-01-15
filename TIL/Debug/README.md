## 2020.12.29
- 갑자기 jupyter tab이 안되고 torch는 지 멋대로 놀고 난리난리
- 별의 별 디버깅 난리에 jupyter 관련 링크 삭제도 해보고
  - https://stackoverflow.com/questions/33052232/how-to-uninstall-jupyter
- tornado downgrade하란 말도 듣고 다른 stackoverflow도 찾아보고
  -  https://stackoverflow.com/questions/33665039/tab-completion-does-not-work-in-jupyter-notebook-but-fine-in-ipython-terminal
  - https://stackoverflow.com/questions/48090119/jupyter-notebook-typeerror-init-got-an-unexpected-keyword-argument-io-l
- 결국 source도 뜯어보려 했으나... 그건 무리
  - gen, tornado, ipython, ipykernel 등등 라이브러리 소스도 봤징
- 그래서 해결한 방법은, 아래 링크들
  - https://github.com/jupyter/notebook/issues/2435
  - https://ipython.readthedocs.io/en/stable/config/intro.html
- 오류 소스 뜯어보니, tab msg를 던지는 와중에 ipython engine에서 오류가 난 것 같더라고
- 어떻게 했냐?
  - `ipython profile create`로 ipython config 파일 생성
  - 생성된 파일로 들어가서 `c.Completer.use_jedi = False` 라인 추가
  - `ImportError: The Jupyter Notebook requires tornado >= 5.0, but you have 4.5.3` 에러가 떠서 tornado upgrade
- 따라란 성공적으로 build


## 2021.01.15
1. PyTorch Detach Error 수정
    ```
    RuntimeError: Trying to backward through the graph a second time, 
    but the saved intermediate results have already been freed. 
    Specify retain_graph=True when calling backward the first time.
    ```
    - 벨만님 오류 수정!
    - 처음에 뭔가 굉장히 많은 링크들을 확인했다 ㅋㅋ LSTMCell 관련
      - https://www.facebook.com/groups/PyTorchKR/permalink/1203101746496171/
      - https://github.com/jinserk/pytorch-asr/blob/master/asr/models/deepspeech_ctc/network.py?fbclid=IwAR1IBgfpeRkyd_Q5QtSc5ynZGs6jeFoqMKcPHTLU3xtJcEL6C5lbsxCqp0Y
      - https://github.com/ctr4si/A-Hierarchical-Latent-Structure-for-Variational-Conversation-Modeling/blob/master/model/layers/rnncells.py?fbclid=IwAR1J4SUTt0N91kA_hA5yU2VHHaFIwSYDsHqW4OJITQxI1D55Y8J5-Momcgk
      - https://github.com/sordonia/zforcing/blob/master/model.py
      - https://discuss.pytorch.org/t/solved-training-a-simple-rnn/9055/14
      - https://discuss.pytorch.org/t/why-i-must-set-retain-graph-true-so-that-my-program-can-run-without-error/12428/2
    - 이 과정에서 정말 많은 것들을 배움...
        ```python
        hidden = hidden[0].detach(), hidden[1].detach()
        ```
    - 그러나 LSTM Cell 문제가 아니었고, 과거 tensor에 접근하는 과정에서 그래프가 꼬였던 것이 문제.
    - NAS 코드도 얻고 디버깅도 하고 유익했다.
2. Pytorch id vs data_ptr
    - 이건 공부거리! 
    - 좀 많이 봐야겠다
    - https://discuss.pytorch.org/t/any-way-to-check-if-two-tensors-have-the-same-base/44310
    - https://wordbe.tistory.com/entry/Pytorch-1-파이토치를-써야하는-이유-텐서란
    - https://stackoverflow.com/questions/62607863/slicing-pytorch-tensors-and-use-of-data-ptr
    - https://stackoverflow.com/questions/62523708/pointer-type-behavior-in-pytorch

  
