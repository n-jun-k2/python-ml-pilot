# Airflowに関する調べもの

- [構成ファイルのリファレンス](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html?highlight=airflow__api__auth_backend)
- [SQLalchemyのURIの指定方法](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls)
- [DAGについて](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html)
- [TASKについて](https://airflow.apache.org/docs/apache-airflow/stable/concepts/tasks.html)


## 構成図

![](https://airflow.apache.org/docs/apache-airflow/stable/_images/arch-diag-basic.png)

- スケジューラ(Scheduler) : スケジュールされたワークフローのトリガーと、実行するタスクのエ クゼキュータへの送信の両方を処理するスケジューラです。
- タスクの実行を処理するエクゼキュータ(Executor) : デフォルトのAirflowインストールでは、スケジューラ内ですべてが実行されますが、ほとんどの実稼働に適したエグゼキュータは、実際にはワーカーにタスク実行をプッシュします。
- ウェブサーバー(Webserver)： DAGとタスクの動作を検査、トリガー、デバッグするための便利なユーザーインターフェイスを提供します。
- スケジューラとエグゼキュータ（およびエグゼキュータが持つすべてのワーカー）が読み込むDAGファイルのフォルダー(DAG directory)
- スケジューラ、エクゼキュータ、ウェブサーバが状態を保存するために使用するメタデータ・データベース。(Metadata Database)

### 主要なワークロード

- Operators：DAGのほどんどの部分を構築する為に素早く連動させることができる定義済みのタスク。
- Sensors:オペレーターの特別なサブクラスで、外部イベントが発生するのを待つだけです。
- TaskFlow-decorated : @taskは、Pythonのカスタム関数をTaskとしてパッケージングしたものです。

基本的に、OperatorとSensorはテンプレートで、DAGファイル内で呼び出すと、Taskを作成していることになります。

### Control Flow:
DAGは何度も実行されるように設計されており、複数回の実行を並行して行うことができる。DAGはパラメータ化されており、常に「実行する」間隔（データ間隔）を含むが、他のオプションのパラメータもある。

タスクは、お互いに依存関係を宣言しています。DAGでは、``>>``演算子や``<<``演算子を使って、これを見ることができます。

※Airflow 1.8以降

```python
first_task >> [second_task, third_task]
third_task << fourth_task
```

※Airflow 1.8より前
```python
first_task.set_downstream([second_task, third_task])
third_task.set_upstream(fourth_task)
```

これらの依存関係は、グラフの「エッジ」を構成するものであり、Airflowがどの順番でタスクを実行するかを決定する方法である。デフォルトでは、タスクはその上流のタスクがすべて成功するまで待ってから実行されますが、これはBranching、LatestOnly、Trigger Rulesなどの機能を使ってカスタマイズすることが可能です。

タスク間でデータを受け渡すには、2つの方法があります。

- XComs（「相互通信」）、タスクに小さなメタデータをプッシュさせたり、プルさせたりできるシステムです。
- ストレージサービス（自社運用、またはパブリッククラウドの一部）から大容量ファイルをアップロード、ダウンロードする。

Airflowは、スペースが空くとWorker上で実行するタスクを送り出すので、DAG内のすべてのタスクが同じWorkerまたは同じマシンで実行される保証はありません。

サブDAGを使えば、他のDAGに埋め込むことができる「再利用可能な」DAGを作ることができますし、タスクグループを使えば、UI上でタスクを視覚的にグループ化することができます。

また、データストアのような中央リソースへのアクセスを、コネクションとフックの形で簡単に事前設定できる機能や、プールを使って同時実行を制限する機能もあります。

## User interface

Airflowは、DAGとそのタスクが何を行っているかを確認し、DAGの実行をトリガーし、ログを表示し、DAGの問題のいくつかの限定的なデバッグと解決を行うことができるユーザーインターフェイスが付属しています。

## タスクインスタンスの状態とライフサイクル:

ライフサイクル

![](https://airflow.apache.org/docs/apache-airflow/stable/_images/task_lifecycle_diagram.png)

状態の一覧

| task state | overview |
| --- | --- |
|none|タスクはまだ実行のためにキューに入れられていません（その依存関係はまだ満たされていません）|
|scheduled|スケジューラーは、タスクの依存関係が満たされていると判断し、実行する必要があります|
|queued|タスクはエグゼキュータに割り当てられており、ワーカーを待っています|
|running|タスクはワーカー（またはローカル/同期エグゼキューター）で実行されています|
|success|タスクはエラーなしで実行を終了しました|
|shutdown|タスクの実行中に、タスクのシャットダウンが外部から要求されました|
|restarting|タスクの実行中に、タスクの再起動が外部から要求されました|
|failed|タスクの実行中にエラーが発生し、実行に失敗しました|
|skipped|分岐、LatestOnly、または同様の理由でタスクがスキップされました。|
|upstream_failed|アップストリームタスクが失敗し、トリガールールに必要であると表示されます|
|up_for_retry|タスクは失敗しましたが、再試行の試行が残っており、再スケジュールされます。|
|up_for_reschedule|タスクはモードになっているセンサーですreschedule|
|sensing|タスクはスマートセンサーです|
|deferred|タスクはトリガーに延期されました|
|removed|実行が開始されてから、タスクはDAGから消えました|
